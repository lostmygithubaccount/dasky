forked from https://github.com/danielsc/azureml-and-dask

# Azure ML and Dask

![Summary gif](media/describe.gif)

## Introduction

Dask + Azure ML = OSS Data Science & ML @ Scale.

## This repo

`AzureMLCluster` makes it easy to setup a powerful Dask cluster for interactive work:

```python
from azureml.core import Workspace
from dask_cloudprovider import AzureMLCluster

ws = Workspace.from_config()
cluster = AzureMLCluster(ws, jupyter=True)
cluster
```

![Widget](media/widget.gif)

See [this notebook](local/01.start-cpu.ipynb) to start up a Dask cluster on Azure ML.
