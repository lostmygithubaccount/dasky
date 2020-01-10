from dask.distributed import Client
from dask_cloudprovider import AMLCluster

from azureml.core import Workspace

ws = Workspace.from_config()

ct = ws.compute_targets['my_compute_target'] # CPU or GPU | vNET or Internet 

env = ws.environments['AzureML-Dask'] # curated environment

cluster = AMLCluster(ct)              # only required input

cluster = AMLCluster(
      ct
    , jupyter=True                                 # start Jupyter Lab on headnode
    , jupyter_token=None                           # set custom Jupyter token
    , datastore_mount='workspacefiledatastore'     # default to default file datastore; for code consistency
    , node_count=None                              # number of nodes if adapt set to False; default = 1
    , adapt=False                                  # turn on adaptivity
    , min_nodes=None # if adapt set to True this indicates min number of nodes to scale from
                     # needs to be greater or equal to the min number of nodes set in the cluster
                     # but less than or equal to the maximum number of nodes
                     # setting to maximum number of nodes should automatically set the max_nodes flag to same
    , max_nodes=None # if adapt set to True this indicates the maximum number of nodes to scale to
                     # needs to be greater or equal to the min number of nodes set in the cluster
                     # but less than or equal to the maximum number of nodes
                     # automatically set to maximum if min_nodes set to maximum nodes provisioned in the cluster
    , env=None # default to 'AzureML-Dask'
        )

cluster.print_jupyter_uri() # print link w/token to Jupyter Lab session

c = Client(cluster) # returns standard Client output - dashboard link + # of nodes, workers, etc.
