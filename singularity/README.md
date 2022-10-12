Instructions for Singularity

Singularity Tutorial: https://singularity-tutorial.github.io/

Before starting:

On OSUT3 make sure you are on interactive-0-0 (this is the only node currently with singularity installed)

Make sure you are a "fakeroot" user. Singularity relies on fakeroot users to install packages
Actual sudo user must do:

singularity config fakeroot --add <username>

Note: on OSUT3 need to also do
echo 10000 > /proc/sys/user/max_user_namespaces

Creating Sandbox:

Download the setup script createContainer.sh
wget https://github.com/carriganm95/milliqanOffline/blob/singularity/singularity/createContainer.sh

Run the script to create a sandbox container
bash createContainer.sh 

Run the container
singularity shell --bind /store:/mnt offline.sif

Now you can run the offline analysis!

Note:
Here /store is a soft link to hadoop storage and needs to be bound to the singularity container. Any links need to be bound to the container this way to access them. 

Note:
Singularity has changed to apptainer so if installing for the first time it is better to install apptainer. If using CMSSW certain versions of will have singularity or apptainer. All singularity commands should be changed to apptainer. 

