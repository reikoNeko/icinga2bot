This project is no longer in development. You are free to fork it for your own use.
icinga2bot is a plugin for errbot that speaks to the Icinga2 API in order to relay messages to and from a chat channel. 

## Caveats
After learning that errbot 4 had trouble with Python 3.5 on Ubuntu, I decided to support only Errbot version 5.x.

Principal development has been done in Centos 7 with python 3.4 and Errbot version 4.1.3, moved to Errbot 5.1.2 on September 25, 2017. I am actively seeking volunteers to help test and port the plugin on other systems.

## Requirements:
* Python 3 >= 3.4 
* External libraries: requests, urllib3
* Errbot from http://errbot.io/en/latest/index.html
* An Icinga2 instance and access to the API 

### Centos 7 requirements:
* Epel Repo in order to get Python 3.4
* Epel packages: python34 python34-tools python34-devel
* Compiler and libraries to build errbot: gcc, glibc-devel, libffi-devel, openssl-devel
* As errbot user:
```
 virtualenv -p python3.4 err
 err/bin/pip install -U setuptools
 err/bin/pip install errbot
```

## Installation Prerequisites

* Activate the [Icinga2 API](https://docs.icinga.com/icinga2/snapshot/doc/module/icinga2/chapter/icinga2-api)
* Install [Errbot](http://errbot.io/en/latest/user_guide/setup.html) 

## Plugin installation
* Assuming your errbot installation directory is /home/errbot, clone or pull the icinga2bot files to /home/errbot/plugins
* Copy the Icinga2 certificate file to /home/errbot/plugins
* Edit icinga2bot.ini to match your configuration
* Add the certificate and icinga2bot.ini to .gitignore, just in case

## Starting the bot

If you have configures your bot according to http://errbot.io/en/latest/user_guide/setup.html, then you can start the bot with 
    ```/path/to/my/virtualenv/bin/errbot --daemon```
and check that it has entered your chatroom. If the plugin has any errors on startup, those will be shown in stderr.

## Using the bot

In channel, icinga2bot accepts the following commands:
* __!i2status__ will show a summary of the state of everything being monitored, e.g.
```
    HOSTS     323 Up; 7 Down; 4 Unreachable
    SERVICES  307 OK;  33 Critical; 3 Warning; 13 Unreachable; 1 Unknown
    Checks per minute:  108 hosts, 83 services, 271 database queries
```
* __!host *hostname*__ will show the up/down state of a single host

From the Icinga2 side, the bot will relay the following events to the chat channel:
* State changes
* Comments
* Problem acknowledgments 
* Notifications sent to a mailing list
* Downtime start, stop, and definition

The easiest way to test these features is to add or remove a comment from an existing host.


