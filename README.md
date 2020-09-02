forked from https://github.com/danielsc/azureml-and-dask

# Azure ML and Dask

![Summary gif](media/describe.gif)

## Introduction

Dask + Azure ML = OSS Data Science & ML @ Scale.

## This repo

`AzureMLCluster` makes it easy to setup a powerful Dask cluster for interactive work. 

There are a few options for starting a Dask cluster on Azure ML Compute.

### managed Compute Target (recommended)

See [local](local) for letting `dask-cloudprovider` take care of creating (and deleting) the Azure ML Compute Target on your behalf. You can specify a `vm_size` and other parameters.

This is recommended to avoid vnet and SSH setup.

### vnet - Compute Instance and Compute Target on same vnet 

If you need your Compute Target on a vnet, it is recommended to use an Azure ML Compute Instance deployed within the same vnet for creating a Dask cluster. 

See [ct-vnet](ci-vnet) for details:

- [01.setup-compute.ipynb](ci-vnet01.setup-compute.ipynb) can be run from anywhere and will create a vnet, Compute Instance on the vnet, and Compute Target on the vnet
- [02.start-cluster.ipynb](ci-vnet/02.start-cluster.ipynb) **must be run on the Compute Instance in the vnet** and creates a Dask cluster from the Compute Target

### Compute Target via SSH

If you'd otherwise like to manage the Compute Target, you need to enable SSH when creating it to allow for tunneling to connect to the Dask cluster.

See [ct-ssh-no-vnet](ct-ssh-no-vnet) for details:

- [01.start-cluster.ipynb](ct-ssh-no-vnet/01.start-cluster.ipynb) can be run from anywhere and will create a pair of SSH public and private keys, Compute Target using the SSH public key, and Dask cluster using the SSH private key
