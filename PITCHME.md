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
are the people who keep the network up and your website answering queries.
+++

Sysadmin on a good day

![Neo dodging bullets](https://i.ytimg.com/vi/ybKJOOmZfMs/maxresdefault.jpg){width: 400px}

+++

Sysadmin on a bad day

![Barely escaping zombies](http://4.bp.blogspot.com/_6Ycg6Y79jFg/TPx0pKhBSPI/AAAAAAAAAwc/e0UyoC3s5KY/s1600/Walking%2BDead.jpg)

+++

Sysadmin on a great day

![Drinking coffee and reading IRC](http://pa1.narvii.com/5669/04e096dee7a5ae3493bde3affb1eed4c81c4d089_hq.gif)

+++

* Really, we just want things to go smooth.

+++

![Kaylee fixin' things](https://archetypeonlinemagazine.files.wordpress.com/2014/06/ariane179254_firefly_1x02_thetrainjob_0002-2.jpg)

Engineers, not captains, make things go smooth.
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
* My team had a Jabber server which we used to communicate.
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

* Nagios was a sysadmin's best friend starting in 1999. It had a web GUI that showed you an overview of server health and could pag eor email you when things were in trouble.

+++

* It didn't just show up/down, but you could apply warning threshholds.

![Nagios status sample](http://my-plugin.de/wiki/_media/check_multi/examples/multi_feeds_passive_sample.png)

+++

* In 2009, Nagios split into Nagios Core and Nagios Enterprise; the former is still GPL, but the latter addons were not open-source.

+++

* As a result, developers began forking Nagios and open-sourcing some workalike Enterprise features; Icinga was one of these.

+++

* Icinga was a direct fork, Icinga2 is a ground-up rewrite with a new API

---

## So we have an API!

* The Icinga2 API sends and receives JSON over HTTPS. 

* Accepts comments and commands

* Sample Python code in icinga.org documentation

* Provides an event stream of all the check results and state changes

---

## JSON is wayyyy too wordy for chat.
```
{"downtime":{"__name":"dbcow22!icinga.local-1493430143-4",
"author":"dbadmin","comment":"DB Tablespace Maintenance",
"config_owner":"","duration":0.0,"end_time":1493606512.0,
"entry_time":1493430143.8262829781,"fixed":true,
"host_name":"dbcow22","legacy_id":4.0,"name":"icinga.local-
1493430143-4","package":"_api","scheduled_by":"",
"service_name":"","start_time":1493430112.0,"templates":
["icinga.local-1493430143-4"],"trigger_time":0.0,
"triggered_by":"","triggers":[],"type":"Downtime",
"version":1493430143.8263230324,"was_cancelled":false,
"zone":""},
"timestamp":1493430143.8306179047,"type":"DowntimeAdded"}
```

becomes

``` 
dbadmin has scheduled downtime for dbcow22 lasting 2 days, 
1:00:00 because DB Tablespace Maintenance 
```
---
### And here's the code that does that
```
def downadd(e):
    d = e["downtime"]
    duration = str(timedelta(seconds=int(
      d["end_time"] - d["start_time"])))
    return "{0} has scheduled downtime for {1} lasting {2} 
      because {3}".format(
      d["author"], downservice(d), duration, d["comment"])
```
---
## Errbot

* Errbot is written in python, has a plugin framework, and talks to multiple chat servers.

* Writing plugin commands is pretty easy because it's done in decorators.

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

* Developed with Python 3.4 on Centos 7

* Tested IN PRODUCTION!

* Because the shoemaker's children got no test box

* <strike>One monolitic python file</strike>

* But, it works.
---
## Frankenstein says what?
Give my creation life!

![Dance, monster, dance!](http://uploads.neatorama.com/wp-content/uploads/2012/07/YFritz.jpg)

---
## Oops. Here come the villagers. I mean the bugs.

![Reality check](http://cdn.hark.com/images/000/439/892/439892/original.jpg)

---
## Monster on the move

* Jabber got dropped in favor of slack -- but errbot supports both!

* Change the errbot config.py file to replace jabber server data with a slack API token

* Bots have to be invited to rooms, so a warning gets logged but nothing tragic.

---
## Got a friend, a victim, a friend!

![User response](https://marruda3.files.wordpress.com/2013/11/young-frankenstein-meal.jpg)

Since promoting the bot on Twitter and at Fosscon, I've gotten my first bug reports!

---

* Had to upgrade my own version of Errbot because the world had passed the original code by. ("It works on my box" is never enough.)
* Don't assume all the world is running mysql.
* Really, really don't assume the order of json fields.

---
* I still have trouble understanding Python threads.
![Obligatory cat picture](https://orig00.deviantart.net/95a2/f/2007/014/1/f/cat_tangled_in_yarn_by_faralight.jpg)
---
## To the future!

* Currently refactoring to separate icinga from bot code

* Writing unit tests

* Using a dedicated VM!

* Seeking help
---
## How to help

* File bug reports

* Add tests, particularly for Jenkins

* Pull requests at https://github.com/reikoNeko/icinga2bot

---
## Further Reading

* https://www.icinga.com/docs/icinga2/latest/doc/12-icinga2-api/

* http://errbot.io/en/latest/

---
## Contact me

* Penth on Freenode (in #plug, #fosscon and #lopsa)

* @LinuxandYarn on Twitter

* https://github.com/reikoNeko/icinga2bot
