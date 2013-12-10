Installation
============

## A Guide to Going from Zero to Server in Just a Bit of Time

Install some things to get you started:

```
$ sudo apt-get update
$ sudo apt-get install python-dev python-rpi.gpio
$ curl -O http://python-distribute.org/distribute_setup.py
$ sudo python distribute_setup.py
$ curl -O https://raw.github.com/pypa/pip/master/contrib/get-pip.py
$ sudo python get-pip.py
$ sudo pip install virtualenv requests
```

Clone the git repository:

```
$ git clone https://github.com/hci-au-dk/whiteboard-camera.git
$ cd whiteboard-camera
```

Next, get your virtual environment up and running either by:

```
$ virtualenv venv --distribute # creates a new virtual environment named "venv"
$ source venv/bin/activate #activates the current environment

$ deactivate #when you are done with your virtual environment - Don't do this yet!
``` 

Next, install the required components:

```
$ sudo apt-get install libjpeg8-dev python-serial python-imaging-tk
$ pip install -r requirements.txt
$ pip install https://github.com/hci-au-dk/picam/zipball/master#egg=picam
```

To finish setting up the thermal printer:

```
$ sudo usermod -a -G dialout pi # permission to dial out
```

Edit `/boot/cmdline.txt` by deleting anything that contains `ttyAMA0`.

Here's what it should look like in the end:

```
dwc_otg.lpm_enable=0 console=tty1 root=/dev/mmcblk0p2 rootfstype=ext4 rootwait
```

We also need to remove/ comment out the last line of `/etc/inittab` (`T0:23:respawn:/sbin/getty -L ttyAMA0 115200 vt100`).

Finally, `sudo shutdown -r now`.

Now, you are ready to run your server. If you want it to run for a long time in a place, I would recommend using `screen`.

```
$ sudo apt-get screen
$ screen -S name_of_your_session # the name can be whatever you like
$ python button-setup.py & # if you have a button and want it to be connected - you'll want this to be run in the background
$ python discontinuityboard.py # you should be able to connect to this server now!
```

To leave your `screen` session and keep your server running, `Ctrl-a d`. You can reattach with the command `screen -r` to see the processes you left running. To see all your screen sessions `screen -ls\
`.

You'll want to have your main server running also for full functionality. See the instructions in `README-DEV.md` in [discontinuityboard](https://github.com/hci-au-dk/discontinuityboard).


## Less Verbose Instructions

To install on a 

    sudo apt-get install python-dev
    curl -O http://python-distribute.org/distribute_setup.py
    python distribute_setup.py
    curl -O https://raw.github.com/pypa/pip/master/contrib/get-pip.py
    python get-pip.py
    sudo pip install virtualenv

And then we need to install the requirements!

    sudo apt-get install libjpeg8-dev
    pip install -r requirements.txt
    pip install https://github.com/hci-au-dk/picam/zipball/master#egg=picam

