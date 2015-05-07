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

import supybot.conf as conf
import supybot.registry as registry
from supybot.i18n import PluginInternationalization, internationalizeDocstring
import os

_ = PluginInternationalization('fearbot')

def configure(advanced):
    from supybot.questions import expect, anything, something, yn
    conf.registerPlugin('fearbot')

fearbot = conf.registerPlugin('fearbot')
conf.registerGlobalValue(fearbot, 'domain',
    registry.String("http://www.reddit.com", """The domain to check. Probably http://www.reddit.com
    unless you've got a different reddit install"""))
    
conf.registerGlobalValue(fearbot, 'checkinterval',
    registry.NonNegativeInteger(5, """How often, in minutes, to check reddit for new posts"""))
    
conf.registerGlobalValue(fearbot, 'redditname',
    registry.String("Reddit", """The name of the reddit install. Not really a big deal. Leave blank
    to not have the [reddit] part of the announce message"""))

conf.registerGlobalValue(fearbot, 'shortdomain',
    registry.String("http://redd.it", """The short domain to use. Probably http://redd.it unless you've
    got your own reddit install. If you don't have a short domain just set it to your long domain"""))
    
conf.registerGlobalValue(fearbot, 'subreddits',
    registry.SpaceSeparatedListOfStrings('#android:android+androidcirclejerk', """A list of subreddits to announce in each channel.
    Format is #channel:subreddit+subreddit+subreddit #channel2:subreddit+subreddit"""))

conf.registerGlobalValue(fearbot, 'configfile',
    registry.String(conf.supybot.directories.data.dirize("fearbot.ini"), """The configuration
    file used for setting up the subreddit/channels"""))
