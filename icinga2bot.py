from errbot import BotPlugin, botcmd, arg_botcmd, webhook
import requests
import json
import configparser
import threading
import re
import logging

from collections import OrderedDict as OD
from socket import gethostbyname, gethostbyaddr, gaierror
from os import path, getcwd
from time import sleep, time
from datetime import timedelta
from urllib3.util.retry import Retry


# botlog.setLevel = logging.DEBUG
logging.basicConfig(filename="/var/log/errbot/icinga2bot.log")
botlog = logging.getLogger('icinga2bot')
botlog.setLevel(logging.INFO)

## Errbot Plugin Config

# One INI file for API host and authentication, user privs.
# There will be no defaults for users specified here, but the default
# 'root', 'icinga2' user and password for the icinga2 api are included
# in the INI file.

default_server= OD(( 
    ('host','localhost'), ('port', '5665'), ('api','v1'),
    ('ca','/etc/icinga2/pki/ca.crt')
    ))
# ConfigParser normally converts all options to lower case but 
# the icinga2 API is case sentitive so we'll add optionxform below.
default_events= OD(( 
    ('CheckResult', 'off'), ('StateChange', 'on'), ('Notification', 'on'),
    ('AcknowledgementSet', 'on'), ('AcknowledgementCleared', 'on'),
    ('CommentAdded', 'on'), ('CommentRemoved', 'on'),
    ('DowntimeAdded', 'on'), ('DowntimeRemoved', 'on'), ('DowntimeTriggered', 'on')
    ))
default_config = OD(( ('server',default_server), ('events',default_events) ))

cfg = configparser.ConfigParser()
cfg.optionxform = str  #make options case-sensitive
cfg.read_dict(default_config)
configfile = path.join(path.dirname(path.realpath(__file__)), 'icinga2bot.ini')
try:
    cfg.read( configfile )
except IOError as E:
    raise("'Cannot find ini file in '+path") from E
except:
    raise
finally:
    print(getcwd())

## Validity Checks

def i2url(host,port,version=default_server['api']):
    ''' Validate host and port, and return the API URL header '''
    try:
        host = gethostbyaddr(gethostbyname(host))[0]
    except gaierror:
        raise ValueError("Could not resolve hostname from configuration. Abandoning.")
    try:
        port = str(int(port))
    except ValueError:
        port = str(default_server['port'])
        print('Port number invalid in config file; falling back to default',port)
    return 'https://'+host+':'+port+'/'+version

try:
    api_auth = (cfg['server']['user'], cfg['server']['password'])
except KeyError:
    raise NameError('Configuration file must have user and password values. Abandoning.')

api_url = i2url(cfg['server']['host'], cfg['server']['port'], cfg['server']['api'])
#botlog.info(api_url)
api_ca  = cfg['server']['ca']

## Establish API session

i2session = requests.session()
i2session.auth = api_auth
i2session.verify = api_ca
i2session.headers  = {
    'Accept': 'application/json',
    }
sess_args = requests.adapters.HTTPAdapter(max_retries = Retry(read=5, connect=10, backoff_factor=1))

try:
    i2session.mount(api_url, sess_args)
    botlog.info("Connected to %s.",api_url)
except (requests.exceptions.ConnectionError,
      requests.packages.urllib3.exceptions.NewConnectionError) as drop:
    botlog.error("No connection to Icinga API. Error received: "+str(drop))
    sleep(5)
    pass


## Helper functions

# Props to Tim Pietzcker
# http://stackoverflow.com/questions/2532053/validate-a-hostname-string
def is_valid_hostname(hostname):
    if len(hostname) > 255:
        return False
    if hostname[-1] == ".":
        hostname = hostname[:-1] # strip exactly one dot from the right, if present
    allowed = re.compile("(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
    return all(allowed.match(x) for x in hostname.split("."))

# Process API json into chat-friendly strings

def comment(e):
    return "Re: {0}, {1} says: '{2}'.".format(
      e["comment"]["host_name"], e["comment"]["author"], e["comment"]["text"])
    
def commentrm(e):
    return "Comment ({0}) removed from {1}".format(
      e["comment"]["text"], e["comment"]["host_name"])
    
def ack(e):
    return "{0} problem on {1} acknowledged by {2}.".format(
      e.get("service","host"), e["host"], e["author"])

def ackrm(e):
    return "Acknowledgement of {0} problem on {1} cleared.".format(
      e.get("service","host"), e["host"])

def notification(e): 
    return "Notice of {0} on {1} sent to {2}".format(
      e["notification_type"], e["host"], e["users"].join(", "))

def state(e):
    before = e['check_result']['vars_before']
    after  = e['check_result']['vars_after']
    # Prevent retry spam before parsing results
    try:
        if after['attempt'] > 1.0:
            return
    except:
        pass
    
    if after['state'] < before['state']:
        change="RECOVERED"
    elif after['state'] > before['state']:
        change="DEGRADED"
    else:
        change="CHANGED"

    return "{0} {1} on {2}: {3}".format(
      e.get("service","host"), change, e["host"], e["check_result"]["output"])

def nice_event(event):
    ''' Parse json objects returned by icinga into chat-friendly text.'''
    nice = {
        'StateChange': state,
        'CommentAdded': comment,
        'CommentRemoved': commentrm,
        'AcknowledgementSet': ack,
        'AcknowledgementCleared': ackrm,
        'Notification': notification,
        }
    return nice[event['type']](event) if event['type'] in nice else event


def i2events(self, events=cfg['events'], url=api_url):
    '''Generates a stream of events from Icinga2 to relay to the channel. 
       CheckResult is disabled, because it's too spammy. Create/delete comments for testing.'''
    url += '/events'
    types = [ key for key in events if events.getboolean(key) and key != 'CheckResult' ]
    data = {"types": types, "queue": "errbot_events" }
    botlog.debug("in i2events, thread is "+threading.currentThread().getName())

    while not self.stop_thread.is_set():
        try:
            self.stream = requests.post(url, 
            auth = api_auth,
            verify = api_ca,
            headers = {'Accept':'application/json', 'X-HTTP-Method-Override':'POST'},
            data=json.dumps(data),
            stream=True)
            
            if self.stream.status_code == 200:
                try:
                    for line in self.stream.iter_lines():
                        botlog.debug('in i2api_request: '+str(line))
                        text = nice_event( json.loads(line.decode('utf-8')) )
                        if text is not None:
                            yield(text)
                except:
                    botlog.warning("Could not produce JSON from "+str(line))
                    #yield("Could not produce JSON from "+str(line))
                    sleep(5)
            else:
                botlog.warning('Received a bad response from Icinga API: '+str(self.stream.status_code))
                print('Icinga2 API connection lost.')
        except (requests.exceptions.ConnectionError,
          requests.packages.urllib3.exceptions.NewConnectionError) as drop:
            botlog.error("No connection to Icinga API. Error received: "+str(drop))
            sleep(5)
            return("No connection to Icinga API.")



class Icinga2bot(BotPlugin):
    """
    Use errbot to talk to an Icinga2 monitoring server.
    """

    def __init__(self, bot):
     super().__init__(bot)
     self.stop_thread = threading.Event()

    def report_events(self):
        '''Relay events from the Icinga2 API to a chat channel. Not interactive.
        The event queues are selected in icinga2bot.ini'''
        while not self.stop_thread.is_set():
            botlog.debug("in report_events, thread is "+threading.currentThread().getName())
            queue = i2events(self)
            for line in queue:
                self.send(self.room,line)
                botlog.info(line)


    def activate(self):
        """
        Triggers on plugin activation
        """
        self.room = self.query_room(self.bot_config.CHATROOM_PRESENCE[0])
        #self.stop_thread = threading.Event()
        self.thread = threading.Thread(target = self.report_events)
        self.thread.setDaemon(True)
        self.thread.start()
        botlog.debug("in activate, thread is "+threading.currentThread().getName())
        super().activate()

    def deactivate(self):
        """
        Triggers on plugin deactivation
        """
        botlog.info('shutting down icinga2bot')
#        try:
#            self.stream.raw._fp.close()
#            botlog.info('API listener closed')
#        except:
#            botlog.warning('API listener did not close.\n'+str(self.events))
        self.stop_thread.set()
        botlog.info('stop_thread.set() complete')
        # Force close event stream, per chat with gbin
        self.thread.join()
        botlog.info('thread.join() complete')
        super().deactivate()


    ## Interactive Commands

    @botcmd
    def i2status(self, msg, args):
        '''Return a summary of host and service states.'''
        room = self.query_room(self.bot_config.CHATROOM_PRESENCE[0])
        i2stat = i2session.get(api_url+"/status").json()
        botlog.info(i2stat)
        try:
            R = i2stat['results'][1]['status']
            for line in (
              "HOSTS     {0} Up; {1} Down; {2} Unreachable".format(
                int(R['num_hosts_up']), 
                int(R['num_hosts_down']), 
                int(R['num_hosts_unreachable']) ),
              "SERVICES  {0} OK;  {1} Critical; {2} Warning; {3} Unreachable; {4} Unknown".format(
                int(R['num_services_ok']), 
                int(R['num_services_critical']), 
                int(R['num_services_warning']), 
                int(R['num_services_unreachable']), 
                int(R['num_services_unknown']) ),
              "Checks per minute:  {0} hosts, {1} services, {2} database queries".format(
                int(R['active_host_checks_1min']), 
                int(R['active_service_checks_1min']),
                int(i2stat['results'][9]['perfdata'][1]['value']) )
            ):
                self.send(room,line)
        except:
            botlog.error("Parsing i2stat failed: "+str(type(i2stat)))
            pass

    @arg_botcmd('hostname', type=str)
    def host(self, msg, hostname=None):
        '''Return the current up/down state of a single host and duration.'''
        room = self.query_room(self.bot_config.CHATROOM_PRESENCE[0])
        if is_valid_hostname(hostname):
            hoststatus = i2session.get(api_url+"/objects/hosts?hosts="+hostname, 
            headers={'X-HTTP-Method-Override':'GET'}
              ).json()
            botlog.info(hoststatus)
            try:
                name = hoststatus['results'][0]['name']
                R = hoststatus['results'][0]['attrs']
                state = ('up','DOWN')[int(R['state'])]
                duration = str(timedelta(seconds=int(time() - R['last_hard_state_change'])))
                if R['flapping']:
                    self.send(room, "{0} is flapping, {1} for {2}".format(name, state, duration))
                else:
                    self.send(room, "{0} has been {1} for {2}".format(name, state, duration))
            except KeyError as E:
                botlog.error(E)
                self.send(room, "No host named {0} was found.".format(hostname))
        else:
            botlog.warning("Shenanigans! Received invalid hostname "+str(hostname))
            self.send(room, "Invalid hostname given.")

