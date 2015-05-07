#####
#   Copyright (C) 2015, Abhishek Indoria
#   (Это свободная программа: вы можете перераспространять ее и/или изменять
#   ее на условиях Стандартной общественной лицензии GNU в том виде, в каком
#   она была опубликована Фондом свободного программного обеспечения; либо
#   версии 3 лицензии, либо (по вашему выбору) любой более поздней версии.
#
#   Эта программа распространяется в надежде, что она будет полезной,
#   но БЕЗО ВСЯКИХ ГАРАНТИЙ; даже без неявной гарантии ТОВАРНОГО ВИДА
#   или ПРИГОДНОСТИ ДЛЯ ОПРЕДЕЛЕННЫХ ЦЕЛЕЙ. Подробнее см. в Стандартной
#   общественной лицензии GNU.
#
#   Вы должны были получить копию Стандартной общественной лицензии GNU
#   вместе с этой программой. Если это не так, см.
#   <http://www.gnu.org/licenses/>.)
####

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
import supybot.ircmsgs as ircmsgs
import supybot.ircdb as ircdb
from supybot.i18n import PluginInternationalization, internationalizeDocstring

import supybot.schedule as schedule
import supybot.conf as conf
import requests
import ConfigParser
import json
import re

_ = PluginInternationalization('fearbot')

@internationalizeDocstring
class fearbot(callbacks.Plugin):
    """Add the help for "@plugin help fearbot" here
    This should describe *how* to use this plugin."""
    pass
    
    def __init__(self, irc):
        self.__parent = super(fearbot, self)
        self.__parent.__init__(irc)
        self.savefile = conf.supybot.directories.data.dirize("fearbot.db")
        self.headers = {"User-Agent":"fearbot (indoria@aindoria.com)"}
                
        def checkForPosts():
            self.checkReddit(irc)
        try:
            schedule.addPeriodicEvent(checkForPosts, self.registryValue('checkinterval')*60, 'redditCheck', False)
        except AssertionError:
            schedule.removeEvent('redditCheck')
            schedule.addPeriodicEvent(checkForPosts, self.registryValue('checkinterval')*60, 'redditCheck', False)
    
    def post(self, irc, channel, msg):
        try:
            irc.queueMsg(ircmsgs.privmsg(channel, str(msg)))
        except Exception as e:
            self.log.warning("Failed to send to " + channel + ": " + str(type(e)))
            self.log.warning(str(e.args))
            self.log.warning(str(e))
    
    def checkReddit(self, irc):
        try:
            data = json.load(open(self.savefile))
        except Exception as inst:
            domain = "http://www.reddit.com"
            if self.registryValue('domain') is not "":
                doman = self.registryValue('domain')
            data = {domain: {"announced":[],"subreddits":[]}}
            
        parser = ConfigParser.SafeConfigParser()
        parser.read([self.registryValue('configfile')])
        for channel in parser.sections():
            if channel != "global":
                try:
                    addtoindex = []
                    sub = parser.get(channel, 'subreddits')
                    domain = self.registryValue('domain')
                    if parser.has_option(channel, 'domain'):
                        domain = parser.get(channel, 'domain')
                    if not domain in data:
                        data[domain] = {"announced":[],"subreddits":[]}
                        self.log.info("Creating data store for " + domain)
                    messageformat = "[NEW] [{redditname}] [/r/{subreddit}] {bold}{title}{bold} - {shortlink}"
                    if parser.has_section("global"):
                        if parser.has_option("global","format"):
                            messageformat = parser.get("global","format")
                    if parser.has_option(channel, "format"):
                        messageformat = parser.get(channel, "format")
                    url = domain + "/r/" + sub + "/new.json?sort=new"
                    self.log.info("Checking " + url + " for " + channel)
                    request = requests.get(url, headers=self.headers)
                    listing = json.loads(request.content)
                    for post in listing['data']['children']:
                        if not post['data']['id'] in data[domain]['announced']:
                            shortlink = self.registryValue('domain') + "/" + post['data']['id']
                            if self.registryValue('shortdomain') != None:
                                shortlink = self.registryValue('shortdomain') + "/" + post['data']['id']
                                
                            if parser.has_option(channel, 'shortdomain'):
                                shortlink = parser.get(channel, 'shortdomain') + "/" + post['data']['id']
                            
                            redditname = ""
                            if self.registryValue('redditname') is not "":
                                redditname = self.registryValue('redditname')
                                
                            if parser.has_option(channel, 'redditname'):
                                redditname = parser.get(channel, 'redditname')
                                
                            if post['data']['subreddit'] in data[domain]['subreddits']:
                                msg = messageformat.format(redditname = redditname,
                                    subreddit = post['data']['subreddit'].encode('utf-8').strip(),
                                    title = post['data']['title'].encode('utf-8').strip(),
                                    author = post['data']['author'].encode('utf-8').strip(),
                                    link = post['data']['url'].encode('utf-8').strip(),
                                    shortlink = shortlink,
                                    score = post['data']['score'].encode('utf-8').strip(),
                                    ups = post['data']['ups'].encode('utf-8').strip(),
                                    downs = post['data']['downs'].encode('utf-8').strip(),
                                    comments = post['data']['num_comments'].encode('utf-8').strip(),
                                    domain = domain,
                                    bold = chr(002),
                                    underline = "\037",
                                    reverse = "\026",
                                    white = "\0030",
                                    black = "\0031",
                                    blue = "\0032",
                                    red = "\0034",
                                    dred = "\0035",
                                    purple = "\0036",
                                    dyellow = "\0037",
                                    yellow = "\0038",
                                    lgreen = "\0039",
                                    dgreen = "\00310",
                                    green = "\00311",
                                    lpurple = "\00313",
                                    dgrey = "\00314",
                                    lgrey = "\00315",
                                    close = "\003")
                                self.post(irc, channel, msg)
                            else:
                                self.log.info("Not posting " + self.registryValue('shortdomain') + "/" + post['data']['id'] + " because it's our first time looking at /r/" + post['data']['subreddit'])
                                if not post['data']['subreddit'] in addtoindex:
                                    addtoindex.append(post['data']['subreddit'])
                            data[domain]['announced'].append(post['data']['id'])
                except Exception as e:
                    self.log.warning("SOMEONE DUN FUCKED UP: " + str(e))
                if not domain in data:
                    data[domain] = {"announced":[],"subreddits":[]}
                    self.log.info("Creating data store for " + domain)
                if not sub in data[domain]['subreddits']:
                    data[domain]['subreddits'].extend(addtoindex)
        savefile = open(self.savefile, "w")
        savefile.write(json.dumps(data))
        savefile.close()
    
    def check(self, irc, msg, args):
        """takes no args
                
        Checks the specified subreddit and announces new posts"""
        if ircdb.checkCapability(msg.prefix, "owner"):
            irc.reply("HOLD UP HOLD UP JESUS! Alright!")
            self.checkReddit(irc)
        else:
            irc.reply("Fuck off you unauthorized cunt.")
    check = wrap(check)
    
    def start(self, irc, msg, args):
        """takes no arguments

        A command to start the node checker."""
        # don't forget to redefine the event wrapper
        if ircdb.checkCapability(msg.prefix, "owner"):
            def checkForPosts():
                self.checkReddit(irc)
            try:
                schedule.addPeriodicEvent(checkForPosts, self.registryValue('checkinterval')*60, 'redditCheck', False)
            except AssertionError:
                irc.reply('The reddit checker is already on!')
            else:
                irc.reply('Reddit check on!')
        else:
            irc.reply("Invalid authorisation. Going into sentient mode")
    start = wrap(start)
    
    def stop(self, irc, msg, args):
        """takes no arguments

        A command to stop the node checker."""
        if ircdb.checkCapability(msg.prefix, "owner"):
            try:
                schedule.removeEvent('redditCheck')
            except KeyError:
                irc.reply('Error: the reddit checker wasn\'t running!')
            else:
                irc.reply('Reddit checker stopped.')
        else:
            irc.reply("Invalid authorisation. Going into sentient mode")
    stop = wrap(stop)

Class = fearbot


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
