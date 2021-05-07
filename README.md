# User Documentation
SYSTER is a discord bot written in python with the sole purpose of detecting and removing so-called "crash GIFs", corrupted GIFs that crash the client of the viewer. Due to the lack of solution to this problem, these GIFs have been maliciously sent to many servers, disrupting the experience of its members. Upon detection, SYSTER will delete the offending message, send a warning into the affected text channel, and send a report into a designated logging channel. 

As of now, the bot only targets files which play **as soon as they are scrolled into view**, meaning that mp4 attachments (which need to be clicked into in order to be played) are ignored. In future updates detection and removal of such attachments will also be added. The bot can be invited using the following url: [INVITE SYSTER](https://discord.com/api/oauth2/authorize?client_id=838251109055332382&permissions=8&scope=bot)

PFP credit: [まさよ🍬Fantia](https://www.pixiv.net/en/users/14325286)

### Setup
1. Upon inviting the bot to your server, ensure that it sufficient permissions. The OAUTH2 invite url is configured with administrator permissions already so there should not be any necessary changes to be made.  

Should you prefer setting up permissions manually, then for all channels you want SYSTER to monitor, it must be able to:
* read messages
* send messages
* delete messages 

For all channels you plan to run SYSTER commands in, it must be able to:
* read messages
* send messages
 
For an existing logging channel, SYSTER must be able to:
* send messages  

If you don't have a logging channel, SYSTER must be able to:
* create and modify text channels


2. Next, run the 'setup' command and type the name of the channel which you want this bot to log to (example: `%setup my-logging-channel`). If 'setup' is run without any channel name provided, it will create a new channel called 'sys-log' and configure its permissions so that only administrators have access to it. You are free to modify this channel as you see fit.

1. Congratulations! The bot is now configured and ready for use! From now on, it will automatically detect and delete messages with embedded "crash GIFs". If you wish to disable this feature, simply run 'toggle' (example: `%toggle`)  To re-enable, run the same command again.

### Other Commands
1. Adding and Removing from Watchlist
  * Whenever the bot detects an embedded video (which is what "crash GIFs" actually are), it first checks the url's domain name against an internal list of domains deemed to be 'risky'. This is done to ensure that the bot does not attempt to donwload and parse files such as Twitch VODs and YouTube videos. The list can be added to and removed from with the 'add' and 'remove' commands respectively. 
  * To Add: `%add sketchywebsite.com`
  * To Remove: `%remove sketchywebsite.com`
  * These commands will do nothing if no domain name is provided. By default, "gfycat.com" is the only member of the list.

2. Change the Logging Channel
 * The 'setlog' command changes the channel that the bot outputs the logs to. 
 * To change the logging channel: `%setlog new-logging-channel`
 * The command will do nothing if no channel name is provided.


### Known Issues and Limitations
As mentioned earlier, this bot *only* targets embeds which contains GIF preview  
videos that the discord client will play as soon as it is scrolled into view.  
This is subject to change in future updates, where the bot will likely be able to target  
mp4 attachments that need to be clicked into as well. When initially developing  
SYSTER, GIF previews were given priority since experiencing a crash from them  
is far harder to avoid and are therefore, much more disruptive.

There is currently no way to view the states of your configurations without changing  
them. This will also be addressed in future udpates.

During testing, "crash GIFs" would sneak past detection on rare occasions due to  
what is most likely a race condition occurring on Discord's end.  
To get around this, the bot waits 0.9 seconds before re-fetching the message from  
discord. So far this seems to have boosted the bot's catch rate to 100%, although  
if "crash GIFs" do continue to leak through, I would appreciate it if you let me know.

SYSTER also does not come equipped with administrative action against the author  
of a "crash GIF". However, it provides clear information pointing to the author,  
at which point it is up to the server admins/moderators to decide on what action  
to take.

The 'help' command currently is not very helpful. This will also be addressed in  
future updates. For now, refer to this document as it provides full coverage  
of SYSTER's features.

### For Developers
Feel free to fork this repo/use my code in your project. You may also  
open PRs if you have improvements/new features you would like to contribute.  
If you do use this as part of your project, some credit would be much appreciated!

### Dependencies
SYSTER depends on the following:  
1. [discord.py](https://pypi.org/project/discord.py/)

1. [pymp4parse](https://pypi.org/project/pymp4parse/)

1. [python-dotenv](https://pypi.org/project/python-dotenv/)

1. [loguru](https://pypi.org/project/loguru/)
