#Setup required VirtualBox and Vagrant
## VirtualBox
VirtualBox is the software that actually runs the VM.
(https://www.virtualbox.org/wiki/Downloads)
Install the *platform package* for your operating system.
You do not need the extension pack or the SDK.
You do not need to launch VirtualBox after installing it.
## Vagrant
Vagrant is the software that configures the VM and lets you share files between
your host computer and the VM's filesystem.
(https://www.vagrantup.com/downloads)
Install the version for your operating system.
## After instalation, cloned this code and do 'vagrant up'.
This may take some time as it set ups the environment.
Then do vagrant ssh, this will enter into Terminal.
go to /vagrant/ and here you can execute the files.

# How to execute ?
## Create a datbase
    run python database_setup.py
    This will create the tables.
## Populate database with some entries.
    Execute python lotsofmenus.py
## Execute the ItemCatalog App
    python project.py
        This will run the flask web server. Then in your broswer (host machine),
        open http://localhost:5000 to view the web page.


* template folder contains all the html files which are rendered from App.