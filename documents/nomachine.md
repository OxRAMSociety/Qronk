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
$ sudo wget [download-url-link]
```

!!! Make sure you download the version that fits your CPU architecture. !!!
You can check your architecture with the command:
```
$ arch
> aarch64
```
Search for your suitable OS and architecture from https://downloads.nomachine.com

Download the package, and unzip with 
```
$ sudo tar zxvf [the-package-name]
```

Then install NoMachine by:
```
$ sudo /usr/NX/nxserver --install
``` 
You need to set the server as active:
```
$ sudo /usr/NX/nxserver --start
```
You should now have NoMachine installed on both computers.

## 3. Connect to target machine from host
You need three things to connect to the target machine's GUI:
1. A user account on the target machine
Unless you have created a user, the default user will be named 'ubuntu', with the password as set above.

2. The ip address of the target machine
You can check the ip address using the command 'ifconfig':
```
# Make sure you're on your VM's shell!
$ ifconfig
enp0s1: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet [ip-address-here] netmask 255.255.255.0  broadcast 192.168.64.255
	...
```
Copy the ip-address down.

3. A window manager on your target machine
GNOME is a default window manager. Install by:
```
$ sudo apt install ubuntu-gnome-desktop
```

You should now be able to connect. From your host computer, open NoMachine and remotely connect by following the rest of the tutorial at:
https://www.nomachine.com/getting-started-with-nomachine


