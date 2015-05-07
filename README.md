This plugin checks a list of subreddits for new posts and announces them in IRC as they come in.

Install the plugin, then configure edit the config file ( `fearbot.ini` in the data directory) in this format:

```ini
[#channel]
subreddits = all
domain = http://www.aindoria.com
shortdomain = http://aindor.ia
redditname = aindoria

[#netsec]
subreddits = android
format = [NEW] [{redditname}] [/r/{subreddit}] {bold}{title}{bold} - {shortlink}
```

The "format" option dictates how the bot should announce messages to the
channel. You can also specify a `[global]` section with a default format.
If none is specificed, the one shown above is used. Available options are:
 
* `{redditname}` - the name of the reddit site. Usually Reddit, but clones
exist

* `{subreddit}` - the name of the subreddit, not including the /r/

* `{title}` - the title of the post

* `{author}` - the user who posted it

* `{link}` - the link that was submitted. For selfposts, this is the long form URL to the comments

* `{shorturl}` - the redd.it short URL

* `{score}` - the current score of the post

* `{ups}` - the number of upvotes it's received

* `{downs}` - the number of downvotes it's received

* `{comments}` - the number of comments it's received

* `{domain}` - the domain of the URL of the post (self.subreddit for selfposts)

* `{bold}` - the code to start or stop bold formatting

* `{underline}` - underline the enclosed text

* `{reverse}` - reverse or italicize the enclosed text (some clients inverse the colors, other italicize)

* `{white}` - make the enclosed text white

* `{colour}` - make the enclosed text in any colour you specify

* `{lcolour}` - make the enclosed text light variant of that colour

* `{dcolour}` - make the enclosed text dark variant of that colour

* `{close}` - resets the color


