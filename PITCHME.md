# Icinga2bot

Stay on top of your servers without leaving IRC!

or

Fill your conversations with interruptions about your flaky network!

---

## What is Chatops?

* Well, system administration is often called "Operations"

* That's led to a bunch of portmanteaus in business speak, where various functions are combined with "ops".
+++
* The biggest is "devops" mixing the responsiblities of developers, who are supposed to make everything new, and operators, who are supposed to keep everything stable.

* You can guess how much fun that creates.
+++
* But we also have "chatops", which lets sysadmins hang out in Jabber, Slack, or IRC without missing important events that happen on their systems, and maybe even solve them without leaving chat!

---

### System administrators

These are the people who keep the network up and your website answering queries.
+++
Sysadmin on a good day

![Neo dodging bullets](https://i.ytimg.com/vi/ybKJOOmZfMs/maxresdefault.jpg)
+++
Sysadmin on a bad day

![Barely escaping zombies](http://4.bp.blogspot.com/_6Ycg6Y79jFg/TPx0pKhBSPI/AAAAAAAAAwc/e0UyoC3s5KY/s1600/Walking%2BDead.jpg)
+++
Sysadmin on a great day

![Drinking coffee and reading twitter](http://pa1.narvii.com/5669/04e096dee7a5ae3493bde3affb1eed4c81c4d089_hq.gif)
+++
* Really, we just want things to go smooth.
+++
![Kayle fixin' things](https://archetypeonlinemagazine.files.wordpress.com/2014/06/ariane179254_firefly_1x02_thetrainjob_0002-2.jpg)
---

## What chatops needs:

* A chat server *with user authentication*.

* A chatbot that talks to that server and has the ability to add new features.

* A monitoring system with a decent API (Application Programming Interface).
+++
* A crazy sysadmin willing to put them together.

* Slightly saner sysadmins asking the crazy one when the bot will work.

---

## Becoming Frankenstein: A Case Study
+++
* My team has a Jabber server we use to communicate.
+++
* We switched our monitoring system from Nagios to Icinga2
+++
* That broke Nagibot, which used to tell us in chat when things went wrong
+++
* We needed a new bot!
+++
* Nagibot was written in Perl. Did not want!

---

## From Nagios to Icinga2: A Brief History

* Nagios begain as NetSaint, but the name was challenged over a similar trademark, so became Nagios
+++
* It was a godsend--actually a Galstead-send--back in 1999, a web gui that showed you an overview of server health and alerted you when things were in trouble.
+++
* Not just up/down, but could apply warning threshholds.

![Nagios status sample](http://my-plugin.de/wiki/_media/check_multi/examples/multi_feeds_passive_sample.png)
+++
* In 2009, Nagios split into Nagios Core and Nagios Enterprise; the former is still GPL, but the latter addons were not open-source.
+++
* As a result, developers began forking Nagios and open-sourcing some workalike Enterprise features; Icinga was one of these.
+++
* Icinga was a direct fork, Icinga2 is a ground-up rewrite with a new API

---

## API, check!

* The Icinga2 API receives REST calls over HTTPS and returns JSON. 

* Accepts comments and commands

* Provides an event stream of all the check results and state changes
+++
* Sample Python code in icinga.org documentation

* Wait, was that Step 2? PROFIT!

---

## That was Step 2!

But there are more steps between here and profit.

![Sad_underpants_gnome](https://images.mauldineconomics.com/images/uploads/ttmygh/8499/image/Gnome%2018p_fmt.png)

---

## JSON is too wordy for chat.
'''
{"downtime":{"__name":"dbcow22!icinga.local-1493430143-4","author":"dbadmin","comment":"DB Tablespace Maintenance","config_owner":"","duration":0.0,"end_time":1493606512.0,"entry_time":1493430143.8262829781,"fixed":true,"host_name":"dbcow22","legacy_id":4.0,"name":"icinga.local-1493430143-4","package":"_api","scheduled_by":"","service_name":"","start_time":1493430112.0,"templates":["icinga.local-1493430143-4"],"trigger_time":0.0,"triggered_by":"","triggers":[],"type":"Downtime","version":1493430143.8263230324,"was_cancelled":false,"zone":""},"timestamp":1493430143.8306179047,"type":"DowntimeAdded"}
'''

becomes

''' dbadmin has scheduled downtime for dbcow22 lasting 2 days, 1:00:00 because DB Tablespace Maintenance 
'''
---
## Errbot

* Errbot is written in python, has a plugin framework, and talks to multiple chat servers.

* Half my work is done! PROFIT!
+++
s/Half/Twenty percent of/
+++
* But seriously, writing plugin commands is pretty easy because it's done in decorators.

```
class HelloWorld(BotPlugin):
    """Example 'Hello, world!' plugin for Errbot"""

    @botcmd
    def hello(self, msg, args):
        """Say hello to the world"""
        return "Hello, world!"
```
---
## Minimum Viable Monster

* Developed w Python 3.4 on Centos 7

* Tested IN PRODUCTION!

* Shoemaker's children got no test box

* One monolitic python file

* But, it works.
---
## Frankenstein says what?

+++
# IT'S ALIIIIIVE!

+++
Unless you're on Debian/Ubuntu.
---

## To the future!

* Currently refactoring to separate icinga from bot code

* Writing unit tests

* Using a dedicated VM!

* Seeking help
---
## How to help

* File bug reports

* Add tests

* Contribute features to the "refactor" branch (TBB)

---
## Contact me

* https://github.com/reikoNeko/icinga2bot

* Penth on Freenode (in #plug and #lopsa)

* @LinuxandYarn on Twitter
---
## Further Reading
* https://www.icinga.com/docs/icinga2/latest/doc/12-icinga2-api/
* http://errbot.io/en/latest/
