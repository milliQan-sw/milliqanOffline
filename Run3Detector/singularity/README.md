# Instructions for Singularity

Singularity Tutorial: https://singularity-tutorial.github.io/

## Before starting:

On OSUT3 make sure you are on interactive-0-0 (this is the only node currently with singularity installed)

Make sure you are a "fakeroot" user. Singularity relies on fakeroot users to install packages
Actual sudo user must do:

`singularity config fakeroot --add <username>`

Note: on OSUT3 need to also do

`echo 10000 > /proc/sys/user/max_user_namespaces`

## Creating Sandbox:

Download the setup script createContainer.sh

`wget https://raw.githubusercontent.com/carriganm95/milliqanOffline/singularity/Run3Detector/singularity/createContainer.sh`

Run the script to create a sandbox container

`bash createContainer.sh <container name> <executable name>`

Run the container

`singularity shell <container name>`

Now you can run the offline analysis!

## Notes:
If you have soft links to storage areas you will need to bind them to the container in order to access them. For example the OSUT3 stores the files in /data (raid storage) or /store (hadoop storage). These both need to be bound to the container by doing

`singularity shell --bind /store,/data <container name>`

Singularity has changed to apptainer so if installing for the first time it is better to install apptainer. If using CMSSW certain versions of will have singularity or apptainer. All singularity commands should be changed to apptainer. 

