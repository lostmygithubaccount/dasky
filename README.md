# Azure ML and Dask 

## Introduction

![Summary gif](media/describe3.gif)

## Create a virtual network 

Create or use an existing virtual network (vNET). Both the interface for the Dask cluster and the cluster itself will be in the virtual network. You can quickly create one in the [Azure Portal](https://docs.microsoft.com/en-us/azure/virtual-network/quick-create-portal) or [Azure CLI](https://docs.microsoft.com/en-us/azure/virtual-network/quick-create-cli) if you do not have one already.

In the `example.ipynb` notebook, the vNET is assumed to be in the same resource group as the workspace with a name 'dask-vnet' and subnet 'default'. 

## Create and setup compute instance 

Create an Azure ML Compute Instance in the vNET you have created. The Virtual Machine (VM) size is unimportant for this blog as it is simply being used as an interface to the Dask cluster and hosting code in the cloud. 

Enabling SSH access is optional.

![Compute instance setup](media/ci-setup.png)

## Launch JupyterLab or Jupyter

Launch JupyterLab (recommended) or Jupyter from the list of URIs. 

![Compute instance URIs](media/ci-jupyterlab.png)

## Clone git repo

Clone the Azure ML and Dask example repo from github. 

You can use the terminal or UI to clone the repo, hosted at https://github.com/lostmygithubaccount/dasky.git. Copy this link and clone the repo.

![Compute instance git setup](media/ci-git-setup.png)

![Compute instance git clone](media/ci-git-clone.png)

![Compute instance git repo](media/ci-git-repo.png)

## Overview of repository 

![Run widget ready](media/run-widget-ready.png)

## Data analysis with Pandas

## Scaling up with Dask

## Scaling up with Dask and Azure ML

## Overview of assets 
