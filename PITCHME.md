# Icinga2bot

Stay on top of your servers without leaving IRC!

or

Fill your conversations with interruptions about your flaky network!

---

# System administrators

* These are the people who keep the network up and your website answering queries.

* Most are customer service oriented, but we have dark dreams...

* ... dreams made famous by "The Bastard Operator from Hell."

* Really, we just want things to go smooth.

---

# Chatops

* System administration is often called "Operations"

* That's led to a bunch of portmanteaus is business speak, where various functions are combined with "ops".

* The biggest is "devops" mixing the responsiblities of developers, who are supposed to make everything new, and operators, who are supposed to keep everything stable.

* You can guess how much fun that creates.

* But we also have chatops, which lets sysadmins hang out in Jabber, Slack, or IRC without missing important events that happen on their systems, and maybe even solve them without leaving chat!

---

# What chatops needs:

* A chat server ''with user authentication''.

* A chatbot that talks to that server and has the ability to add new features.

* A monitoring system with a decent API.

* A crazy sysadmin willing to put them together.

* Slightly saner sysadmins asking the crazy one when Frankenstein's gonna walk.

---

# Becoming Frankenstein: A Case Study

* My team has a Jabber server we use to communicate.

* We switched out monitoring system from Nagios to Icinga2

* That broke Nagibot, which used to tell us in chat when things went wrong

* We needed a new bot!

* Nagibot was written in Perl. Did not want!

---

# From Nagios to Icinga2: A Brief History

* Nagios begain as NetSaint, but the name was challenged over a similar trademark, so became Nagios

* It was a godsend--actually a Galstead-send--back in 1999, a web gui that showed you an overview of server health and alerted you when things were in trouble.

* Not just up/down, but could apply warning threshholds.

* In 2009, Nagios split into Nagios Core and Nagios Enterprise; the former is still GPL, but the latter addons were not open-source.

* As a result, developers began forking Nagios and open-sourcing some workalike Enterprise features; Icinga was one of these.

* Icinga was a direct fork, Icinga2 is a ground-up rewrite with a new API

* Can still use NRPE plugins but is suggesting users run custom checks over SSH instead.

---

# API, check!

* The Icinga2 API receives REST calls over HTTPS and returns JSON. 

* Accepts comments and commands

* Provides an event stream of all the check results and state changes

* Sample Python code in icinga.org documentation

* Wait, was that Step 2? PROFIT!

---

# That was Step 2!

But there are more steps between here and profit.

[img: Sad_underpants_gnome.png]

---

# The Bot

* Errbot is written in python, has a plugin framework, and talks to multiple chat servers.

* Half my work is done! PROFIT!

** s/Half/Twenty percent of/

* But seriously, writing plugin commands is pretty easy because it's done in decorators.

```class HelloWorld(BotPlugin):
    """Example 'Hello, world!' plugin for Errbot"""

    @botcmd
    def hello(self, msg, args):
        """Say hello to the world"""
        return "Hello, world!"
```

---


