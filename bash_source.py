import telebot
import time
import subprocess

print("_  ,_       \n ,'  `\,_   \n |_,-'_)    \n /##c '\  ( \n' |'  -{.  )\n  /\__-' \[]\n /`-_`\     \n '     \    ")

# messages 
info_message= "This bot is using the sherlock project to find links! \norginal creator : Siddharth Dushantha \nyou can find the sherlock project in the link below \n https://github.com/sherlock-project/sherlock"
help_message = "Hunt down social media accounts by username across social networks \nusage \n  send me the Id you whish to search for with the @ \n  example : @sherlock "
start_message = "Hello ! \nI can help you find an specific ID on different social media! \njust send me the ID with @ \n use /help for more info"
not_ready_message = "plaese wait im trying to see what i can find ..."
space_err_message = "please send the username only \n(no space in the message)"

#token
bot_token = ''

#creating necessary objs
#log_size will be the total numbers of lines in log.txt

log_size = 80
admins=[]
bot = telebot.TeleBot(bot_token)

def log_add (user_id,message_text):
    global log_size
    now= time.gmtime()
    time_string=str(now.tm_year)+'/'+str(now.tm_mon)+'/'+str(now.tm_mday)+' @ '+str(now.tm_hour)+':'+str(now.tm_min)+':'+str(now.tm_sec)

    with open("log.txt" , 'a') as log:
        #TODO : log max size limit
        log_string = time_string + "-" + str(user_id) + "-"  + message_text+'\n'
        log.write(log_string)
        log.close()
   


#message handlers
@bot.message_handler(commands = ['start'])
def send_welcome (message):
    global start_message
    bot.reply_to(message, start_message)
    log_add(message.from_user.id,message.text)


@bot.message_handler(commands = ['help'])
def send_help (message):
    global help_message
    bot.reply_to(message , help_message)
    log_add(message.from_user.id,message.text)


@bot.message_handler(commands = ['info'])
def send_info (message):
    global info_message
    bot.reply_to(message , info_message)
    log_add(message.from_user.id,message.text)




@bot.message_handler(func=lambda msg: msg is not None and '@' in msg.text)
def seach_id (message):

    global not_ready_message , space_err_message
    bot.reply_to(message , not_ready_message)

    #this if is to stop people from running any command in the bash session
    if ' ' in message.text:
        bot.reply_to(message , space_err_message)

    else:
        user_id = message.from_user.id
        command=('python3 sherlock '+message.text[1:])

        search_resaults = subprocess.run(command, capture_output= True , shell= True)
        bot.reply_to(message , search_resaults.stdout)

        subprocess.run("rm "+message.text[1:]+".txt",capture_output=True , shell = True)
        log_add(message.from_user.id,message.text)

#TODO : add a add_admin command and func

@bot.message_handler(commands = ['shutdown'])
def shutdown(message):
    global admins
    user_id = message.from_user.id
    
    if admins.count(user_id)!=0:
        #shutdown notifier
        bot.reply_to(message,"shutting down the bot (UwU) ...")
        for admin in admins:
            bot.send_message(admin,"shutdown rquested by "+str(message.from_user.id))
        print("shutdown rquested by "+str(admin))
        log_add(message.from_user.id,message.text)
        bot.stop_bot()
    else:
        bot.reply_to(message , "You are not my admin!")

#running
print("started the bot waiting for any messages!")
quit_while = 0
while True :
    try :
        bot.polling()
        quit_while =0
    except Exception:
        time.sleep(15)
        quit_while +=1
    if quit_while == 2 :
        break