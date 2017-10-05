# -*- coding: utf8 -*-
#incoming bot script

import os;
import sys;
import cfg;
import socket;
import re;
import time;


reload(sys);
sys.setdefaultencoding('utf8');

def chat(sock, msg):
	"""
	Send a chat message to the server.
	Keyword arguments:
	sock -- the socket over which to send the message
	msg  -- the message to be sent
	"""
	global lines;
	global chan;
	if not antiSpam() :
		sock.send("PRIVMSG {} :{}".format(chan, msg).encode("utf-8"));
		print "msg : "+msg;

def whisper(sock,user,msg):
	global lines;
	global chan;
	if not antiSpam() :
		sock.send("PRIVMSG {} :{}".format(chan, ".w "+msg).encode("utf-8"));
		print "msg : "+msg;
	
def ban(sock, user):
    """
    Ban a user from the current channel.
    Keyword arguments:
    sock -- the socket over which to send the ban command
    user -- the user to be banned
    """
    chat(sock, ".ban {}".format(user));

def timeout(sock, user, secs=300):
    """
    Time out a user for a set period of time.
    Keyword arguments:
    sock -- the socket over which to send the timeout command
    user -- the user to be timed out
    secs -- the length of the timeout in seconds (default 600)
    """
    chat(sock, ".timeout {}".format(user, secs));
	
def antiSpam():
	global startTime;
	interval = time.time() - startTime;	
	print interval;
	if interval <= 1.5 :
		print "\n\n SPAM LIMIT REACHED\n\n";
		return True;
	elif interval >1.5 :
		print "reset time and lines";
		startTime = time.time();
		interval = 0;
		return False;
	print "antiSpam unknown error (out of conditions)";
	return True;

prevMessage = "";
Pass = cfg.PASS;
Nick = cfg.NICK;
account_nb = input("1 : Antha | 2 : bot1 :| 3 : bot2 :\n");
if account_nb == 1 :
	pass;
elif account_nb == 2 :
	Pass = cfg.PASS1;
	Nick = cfg.NICK1;
elif account_nb == 3 :
	Pass = cfg.PASS2;
	Nick = cfg.NICK2;
chan = "#";
chan = chan + raw_input("Channel a rejoindre :");
startTime = time.time();
s = socket.socket();
s.connect((cfg.HOST, cfg.PORT));
s.send("PASS {}\r\n".format(Pass).encode("utf-8"));
s.send("NICK {}\r\n".format(Nick).encode("utf-8"));
s.send("JOIN {}\r\n".format(chan).encode("utf-8"));

CHAT_MSG=re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :");
while True:
    response = s.recv(1024);
    if response == "PING :tmi.twitch.tv\r\n":
        s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"));
    else:
		username = re.search(r"\w+", response).group(0); # return the entire match
		message = CHAT_MSG.sub("", response);
		
		#Reading chat
		if "PRIVMSG" in response :
			print username+": "+ message.encode(sys.stdout.encoding, errors='replace');
		
		#shutdown 
			if ("!off") in message.lower() and username == "anthagonas":
				print "\n\n GOING OFFLINE NOW";
				exit();	
				
		#Spam mode		
			if ("!spam") in message.lower() and username == "anthagonas":
				chat(s,re.sub('!spam'," ",message));

