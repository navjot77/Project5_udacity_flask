# Project5_udacity_flask
![image_readme](https://cloud.githubusercontent.com/assets/15641327/20195711/7d769c0c-a74c-11e6-9bdf-61b1e0d546c6.png)

#Setup required VirtualBox and Vagrant

## VirtualBox
VirtualBox is the software that actually runs the Virtual Machine.
Download from :https://www.virtualbox.org/wiki/Downloads
Install the *platform package* for your operating system.
You do not need the extension pack or the SDK.
You do not need to launch VirtualBox after installing it.

## Vagrant
Vagrant is the software that configures the VM and lets you share files between
your host computer and the VM's filesystem.
Download from : https://www.vagrantup.com/downloads
Install the version for your operating system.

## After instalation, cloned this code and do 'vagrant up'.
This may take some time as it set ups the environment.
Then do vagrant ssh, this will enter into Terminal.
go to /vagrant/ and here you can ls and find all files related to project.

# How to run an Application?
## Firstly, Create a datbase
    Execute database_setup.py
    This will create the database and tables.
## Populate database with some entries.
    Execute: lotsofmenus.py
## Execute the ItemCatalog App
    python project.py
        This will run the flask web server. Then in your broswer
        (host machine), open http://localhost:5000 to view the web page.

* template folder contains all the html files which are rendered from App.
