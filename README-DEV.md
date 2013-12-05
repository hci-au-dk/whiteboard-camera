Installation
============

## A Guide to Going from Zero to Server in Just a Bit of Time

Install some things to get you started:

```
$ sudo apt-get install python-dev
$ curl -O http://python-distribute.org/distribute_setup.py
$ python distribute_setup.py
$ curl -O https://raw.github.com/pypa/pip/master/contrib/get-pip.py
$ python get-pip.py
$ sudo pip install virtualenv
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
$ sudo apt-get install libjpeg8-dev
$ pip install -r requirements.txt
$ pip install https://github.com/hci-au-dk/picam/zipball/master#egg=picam
```

Now, you are ready to run your server. If you want it to run for a long time in a place, I would recommend using `screen`.

```
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

