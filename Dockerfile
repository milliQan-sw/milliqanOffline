# Filename: dockerFile

FROM centos:centos7

RUN yum -y install epel-release
RUN yum -y install which

RUN yum -y install emacs-nox
RUN yum -y install git
RUN yum -y install cmake3

RUN yum -y install gcc
RUN yum -y install kernel-devel

RUN yum -y install llvm llvm-devel llvm-static

ENV PYTHON=36
RUN yum -y install vim-X11 vim-common vim-enhanced vim-minimal
RUN yum -y install python${PYTHON} python${PYTHON}-devel python${PYTHON}-pip python${PYTHON}-tkinter
RUN yum -y install python2 python2-devel python2-pip

RUN yum -y install openssl-devel
RUN yum -y install openssh-server openssh-clients
RUN yum -y install rsh rsh-server
RUN yum -y install boost boost-devel

RUN yum -y install xorg-x11-apps
RUN yum install -y lapack-devel blas-devel

RUN yum -y install root
RUN yum -y install python3-root

RUN yum -y install make

RUN python3 -m pip install pymongo
RUN python3 -m pip install pymongo[srv]

