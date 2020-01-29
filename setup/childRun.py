import os
import sys
import uuid
import time
import socket
import argparse
import threading
import subprocess

from mpi4py import MPI
from azureml.core import Run
from notebook.notebookapp import list_running_servers

def flush(proc, proc_log):
    while True:
        proc_out = proc.stdout.readline()
        sys.stdout.write(proc_out)
        proc_log.write(proc_out)
        proc_log.flush()

if __name__ == '__main__':
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    print("commonand ", comm)
    
    parser = argparse.ArgumentParser()
    args, unparsed = parser.parse_known_args()
    
    scheduler_ip = unparsed[3]
    print("scheduler_ip is: ", scheduler_ip)
    
    ip = socket.gethostbyname(socket.gethostname())
    
    print("- my rank is ", rank)
    print("- my ip is ", ip)
        
   
    cmd = "dask-worker " + scheduler_ip 
    worker_log = open("worker_{rank}_log.txt".format(rank=rank), "w")
    worker_proc = subprocess.Popen(cmd.split(), universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    flush(worker_proc, worker_log)
