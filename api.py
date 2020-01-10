from dask.distributed import Client
from dask_cloudprovider import AMLCluster

from azureml.core import Workspace

ws = Workspace.from_config()

ct = ws.compute_targets['my_compute_target'] # CPU or GPU | vNET or Internet 

env = ws.environments['AzureML-Dask'] # curated environment

cluster = AMLCluster(ct) # only required input

cluster = AMLCluster(ct,
        jupyter=True, # start Jupyter Lab on headnode
        jupyter_token=None, # set custom Jupyter token
        datastore_mount=None, # default to default file datastore; for code consistency
        nodes=None, # initial number of nodes; default 0? 1? 
        adapt=True, # turn on adaptivity 
        env=None, # default to 'AzureML-Dask'
        )

cluster.print_jupyter_into() # print link w/ token to Jupyter Lab session

c = Client(cluster) # returns standard Client output - dashboard link + # of nodes, workers, etc.
        



