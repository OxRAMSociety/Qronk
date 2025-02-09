# Installing nomachine

## NoMachine
NoMachine is an application that allows you to remotely connect to a networked computer. In our case, we will be using this to connect from the host machine (your default computer) to the target machine (your newly installed virtual machine).

Follow the documentation here to get install nomachine:
https://www.nomachine.com/getting-started-with-nomachine

## 1. Install nomachine on your host machine

## 2. Install nomachine on your target machine
You need to set a password for your VM. This is done by:
```
$ sudo passwd
```
The command will ask for a new password (it won't display what you type, but it's typing), and for you to confirm it.

You will likely not have GUI access to your target machine. If you have installed via Multipass, you can access the shell using:
```
$ multipass shell [your-instance-name]
```

You should be on your VM's shell. You can download nomachine using the wget command:
```
$ cd /usr
$ wget [download-url-link]
```

The link https://download.nomachine.com/download/8.16/Linux/nomachine_8.16.1_1_i686.tar.gz should work.
Download the package, and unzip with 
```
$ sudo tar zxvf [the-package-name]
```

Then install NoMachine by:
```
$ sudo /usr/NX/nxserver --install
``` 
You should now have NoMachine installed on both computers.

## 3. Connect to target machine from host
To connect, you need a user account on the target machinen as well as the ip address of the machine. Unless you have created a user, the default user will be named 'ubuntu', with the password as set above.
You can check the ip address using the command 'ifconfig':
```
# Make sure you're on your VM's shell!
$ ifconfig
enp0s1: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet [ip-address-here] netmask 255.255.255.0  broadcast 192.168.64.255
	...
```
Copy the ip-address down.

