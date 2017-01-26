This is a work in progress.

icinga2bot is a plugin for errbot that speaks to the Icinga2 API in order to relay messages to and from a chat channel. 

## Requirements:
* Python 3 >= 3.4 
 * External libraries: requests, urllib3
* Errbot from http://errbot.io/en/latest/index.html
* An Icinga2 instance and access to the API 

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


