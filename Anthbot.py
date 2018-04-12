# -*- coding: utf8 -*-
#incoming bot script

import os
import sys
import cfg
import socket
import re
import time


reload(sys)
sys.setdefaultencoding('utf8')

def chat(sock, msg):
	"""
	Send a chat message to the server.
	Keyword arguments:
	sock -- the socket over which to send the message
	msg  -- the message to be sent
	"""
	sock.send("PRIVMSG {} :{}".format(cfg.CHAN, msg).encode("utf-8"))
	print "msg : "+msg

def whisper(sock,user,msg):
	sock.send("PRIVMSG {} :{}".format(user, msg).encode("utf-8"))
	print "msg : "+msg
	
def ban(sock, user):
    """
    Ban a user from the current channel.
    Keyword arguments:
    sock -- the socket over which to send the ban command
    user -- the user to be banned
    """
    chat(sock, ".ban {}".format(user))

def timeout(sock, user, secs=600):
    """
    Time out a user for a set period of time.
    Keyword arguments:
    sock -- the socket over which to send the timeout command
    user -- the user to be timed out
    secs -- the length of the timeout in seconds (default 600)
    """
    chat(sock, ".timeout {} {}".format(user, secs))


hi_mode = False
Pass = cfg.PASS
Nick = cfg.NICK
account_nb = input("1 : Antha | 2 : bot1 :\n")
if account_nb == 1 :
	pass
elif account_nb == 2 :
	Pass = cfg.PASS1
	Nick = cfg.NICK1
chan = "#"
chan = chan + raw_input("Channel a rejoindre :")
cfg.CHAN = chan
startTime = time.time()
lines = 0
s = socket.socket()
s.connect((cfg.HOST, cfg.PORT))
s.send("PASS {}\r\n".format(Pass).encode("utf-8"))
s.send("NICK {}\r\n".format(Nick).encode("utf-8"))
s.send("JOIN {}\r\n".format(chan).encode("utf-8"))

CHAT_MSG=re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")
while True:
    response = s.recv(1024)
    if response == "PING :tmi.twitch.tv\r\n":
        s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
    else:
		username = re.search(r"\w+", response).group(0) # return the entire match
		message = CHAT_MSG.sub("", response)
		
		#Reading chat
		if "PRIVMSG" in response :
			print "MSG from "+username+": "+message.encode(sys.stdout.encoding, errors='replace')
		
		#shutdown 
			if ("!off") in message.lower() and username == "anthagonas":
				print "\n\n GOING OFFLINE NOW"
				exit()	
				
		#hi mode
			if ("!oiii") in message.lower() and username == "anthagonas":
				hi_mode = True
				print "\n\nHI MODE ACTIVATED\n\n"
			if ("! elah") in message.lower() and username == "anthagonas":
				hi_mode = False
				print "\n\nHI MODE DEACTIVATED\n\n"
			if ("antha") in message.lower() and hi_mode == True :
				print "\n\nsaying hi to : "+username+"\n\n"
				chat(s,re.sub('(anthagonas|antha|Anthagonas|Antha)',username,message))
				
		#Viewbot hi 		
			if ("! MrDestructoid") in message and username == "anthagonas":	
				chat(s,'MrDestructoid I\'m here, master\r\n')
				
		#Cohhcarnage !enter 
			if ("closing in TWO minutes, get your entries in by typing !enter if you have not already entered.") in message and username == "cohhilitionbot" :			
				print "\n\nentering cohh giveaway\n\n"
				chat(s,"!enter\r\n")
			
		#Scaythly NepSmug
			if ((message.rstrip() == "nepSmug") or (message.rstrip() == "nepSmug ")) and username == "fearswe":
				chat(s,"nepSmug nepSmug\r\n")