FROM rapidsai/rapidsai:latest
MAINTAINER todrabas@microsoft.com

USER root:root

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
ENV DEBIAN_FRONTEND noninteractive
ENV LD_LIBRARY_PATH "/usr/local/cuda/extras/CUPTI/lib64:${LD_LIBRARY_PATH}"

# Install Common Dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    # SSH and RDMA
    libmlx4-1 \
    libmlx5-1 \
    librdmacm1 \
    libibverbs1 \
    libmthca1 \
    libdapl2 \
    dapl2-utils \
    openssh-client \
    openssh-server \
    iproute2 && \
    # Others
    apt-get install -y \
    build-essential \
    bzip2 \
#    git=1:2.7.4-0ubuntu1.6 \
    wget \
    cpio && \
    apt-get clean -y && \
    rm -rf /var/lib/apt/lists/*

# Intel MPI installation
ENV INTEL_MPI_VERSION 2018.3.222
ENV PATH $PATH:/opt/intel/compilers_and_libraries/linux/mpi/bin64
RUN cd /tmp && \
    wget -q "http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/13063/l_mpi_${INTEL_MPI_VERSION}.tgz" && \
    tar zxvf l_mpi_${INTEL_MPI_VERSION}.tgz && \
    sed -i -e 's/^ACCEPT_EULA=decline/ACCEPT_EULA=accept/g' /tmp/l_mpi_${INTEL_MPI_VERSION}/silent.cfg && \
    cd /tmp/l_mpi_${INTEL_MPI_VERSION} && \
    ./install.sh -s silent.cfg --arch=intel64 && \
    cd / && \
    rm -rf /tmp/l_mpi_${INTEL_MPI_VERSION}* && \
    rm -rf /opt/intel/compilers_and_libraries_${INTEL_MPI_VERSION}/linux/mpi/intel64/lib/debug* && \
    echo "source /opt/intel/compilers_and_libraries_${INTEL_MPI_VERSION}/linux/mpi/intel64/bin/mpivars.sh" >> ~/.bashrc

RUN source activate rapids && \
    pip install --upgrade azureml-sdk && \
    conda install -n rapids matplotlib && \
    pip install cugraph-cuda100 && \
    pip install scapy && \
    pip install mpi4py