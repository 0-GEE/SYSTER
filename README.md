# User Documentation
SYSTER is a discord bot written in python with the sole purpose of detecting  
and removing so-called "crash GIFs", corrupted GIFs that crash the client of
the viewer. Due to the lack of solution to this problem, these GIFs have been
maliciously sent to many servers, disrupting the experience of its members.
Upon detection, SYSTER will delete the offending message, send a warning into
the affected text channel, and send a report into a designated logging channel. 

As of now, the bot only targets files which play **as soon as they are scrolled  
into view**, meaning that mp4 attachments (which need to be clicked into in order  
to be played) are ignored. In the near future I will likely implement detection and removal  
for attachments as well.  
The bot can be invited using the following url: [INVITE SYSTER](https://discord.com/api/oauth2/authorize?client_id=838251109055332382&permissions=8&scope=bot)

### Setup
1. Upon inviting the bot to your server, ensure that it has administrator permissions. The OAUTH invite url is configured with administrator permsssions already so there should not be any necessary changes to be made.

1. Next, run the 'setup' command and type the name of the channel which you want this bot to log to (example: `%setup my-logging-channel`). If 'setup' is run without any channel name specified, it will create a new channel called 'sys-log' and configure its permissions so that only administrators have access to it. You are free to modify this channel as you see fit.

1. Congratulations! The bot is now configured and ready for use! From now on, it will automatically detect and delete messages with embedded "crash GIFs". If you wish to disable this feature, simply run 'Ptoggle' (example: `%Ptoggle`)  To re-enable, run the same command again.

### Commands
Whenever the bot detects an embedded video (which is what "crash GIFs" actually are), it first checks the url's domain name against an internal list of domains deemed to be 'risky'. This so-called 'risk-list' can be added to and removed from with the 'add' (example: `%add sketchywebsite.com`) and 'remove' (example: `%remove sketchywebsite.com`) commands, respectively. The command will do nothing if no domain name is provided. By default, "gfycat.com" is the only member of the list.

Should you wish to change the logging channel of the bot at any point, you can do so using the 'setlog' command. (example: `%setlog new-logging-channel`) The command will do nothing if no channel name is provided.


### Known issues and limitations
As mentioned earlier, this bot *only* targets embeds which contains GIF preview  
videos that the discord client will play as soon as it is scrolled into view.  
This is subject to change in future updates, where the bot will likely be able to target  
mp4 attachments that need to be clicked into as well. When initially developing  
SYSTER, GIF previews were given priority since experiencing a crash from them  
is far harder to avoid and are therefore, much more disruptive.

There is currently no way to view the states of your configurations without changing  
them. This will also be addressed in future udpates.

During testing, "crash GIFs" would sneak past detection on rare occasions due to  
what is most likely a race condition occurring on Discord's end.  If discord's  
servers cannot create the embed fast enough, then the message object sent to SYSTER  
may not contain any embed at all despite all other users being able to see it.  
To get around this, the bot waits 0.9 seconds before re-fetching the message from  
discord. So far this seems to have boosted the bot's catch rate to 100%, although  
if "crash GIFs" do continue to leak through, I would appreciate it if you let me know.

### For Developers
Feel free to fork this repo/use my code in your project. You may also  
open PRs if you have improvements/new features you would like to contribute.  
If you do use this as part of your project, some credit would be much appreciated!

