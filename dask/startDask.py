### Imports
from mpi4py import MPI
import os
import argparse
import time
from dask.distributed import Client
from azureml.core import Run
import sys, uuid
import threading
import subprocess
import socket

from notebook.notebookapp import list_running_servers

def flush(proc, proc_log):
    while True:
        proc_out = proc.stdout.readline()
        if proc_out == '' and proc.poll() is not None:
            proc_log.close()
            break
        elif proc_out:
            sys.stdout.write(proc_out)
            proc_log.write(proc_out)
            proc_log.flush()

if __name__ == '__main__':
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()

    parser = argparse.ArgumentParser()
    parser.add_argument("--datastore")
    parser.add_argument("--jupyter_token", default=uuid.uuid1().hex)
    parser.add_argument("--script")

    parser.add_argument("--dashboard_port", default=9797)
    parser.add_argument("--jupyter_port", default=9999)
    parser.add_argument("--ci_hostname")
    parser.add_argument("--ci_ip")

    args, unparsed = parser.parse_known_args()
    
    ip = socket.gethostbyname(socket.gethostname())
    
    print("- my rank is ", rank)
    print("- my ip is ", ip)
        
    if rank == 0:
        data = {
            "scheduler"  : ip + ":8786",
            "dashboard"  : ip + ":8787"
            }
    else:
        data = None
        
    data = comm.bcast(data, root=0)
    scheduler = data["scheduler"]
    dashboard = data["dashboard"]
    print("- scheduler is ", scheduler)
    print("- dashboard is ", dashboard)
    

    print("args: ", args)
    print("unparsed: ", unparsed)
    print("- my rank is ", rank)
    print("- my ip is ", ip)
    
    if rank == 0:
        Run.get_context().log('headnode', ip)
        Run.get_context().log('scheduler', scheduler) 
        Run.get_context().log('dashboard', dashboard)
        Run.get_context().log('datastore', args.datastore)

        cmd = ("jupyter lab --ip 0.0.0.0 --port 8888" + \
                          " --NotebookApp.token={token}" + \
                          " --allow-root --no-browser").format(token=args.jupyter_token)
        jupyter_log = open("jupyter_log.txt", "a")
        jupyter_proc = subprocess.Popen(cmd.split(), universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        jupyter_flush = threading.Thread(target=flush, args=(jupyter_proc, jupyter_log))
        jupyter_flush.start()

        while not list(list_running_servers()):
            time.sleep(5)

        jupyter_servers = list(list_running_servers())
        assert (len(jupyter_servers) == 1), "more than one jupyter server is running"

        dashboard_forward = subprocess.Popen(["/usr/bin/socat", 
                             	 "tcp-listen:{},fork".format(8787), 
                             	 "tcp:{}:{}".format(args.ci_ip, args.dashboard_port)],
                            	 stderr=subprocess.PIPE, stdout=subprocess.PIPE, universal_newlines=True)
 
        jupyter_forward = subprocess.Popen(["/usr/bin/socat", 
                             	 "tcp-listen:{},fork".format(8888), 
                                 "tcp:{}:{}".format(args.ci_ip, args.jupyter_port)],
                            	 stderr=subprocess.PIPE, stdout=subprocess.PIPE, universal_newlines=True)
 
        Run.get_context().log('dashboard-url', 'https://{}-{}.{}.instances.azureml.net/status'.format(args.ci_hostname, args.dashboard_port, Run.get_context().experiment.workspace.get_details()['location']))
        Run.get_context().log('jupyter-url', 'https://{}-{}.{}.instances.azureml.net/lab?token={}'.format(args.ci_hostname, args.jupyter_port, Run.get_context().experiment.workspace.get_details()['location'], args.jupyter_token))

        cmd = "dask-scheduler " + "--port " + scheduler.split(":")[1] + " --dashboard-address " + dashboard
        scheduler_log = open("scheduler_log.txt", "w")
        scheduler_proc = subprocess.Popen(cmd.split(), universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        cmd = "dask-worker " + scheduler 
        worker_log = open("worker_{rank}_log.txt".format(rank=rank), "w")
        worker_proc = subprocess.Popen(cmd.split(), universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        worker_flush = threading.Thread(target=flush, args=(worker_proc, worker_log))
        worker_flush.start()

        if(args.script):
            command_line = ' '.join(['python', args.script]+unparsed)
            print('Launching:', command_line)
            exit_code = os.system(command_line)
            print('process ended with code', exit_code)
            print('killing scheduler, worker and jupyter')
            #jupyter_proc.kill()
            scheduler_proc.kill()
            worker_proc.kill()
            exit(exit_code)
        else:
            flush(scheduler_proc, scheduler_log)
    else:
        cmd = "dask-worker " + scheduler 
        worker_log = open("worker_{rank}_log.txt".format(rank=rank), "w")
        worker_proc = subprocess.Popen(cmd.split(), universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        flush(worker_proc, worker_log)
