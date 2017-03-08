import config
import urllib2
import json
import time
import thread
from time import sleep

REQUEST_HEADERS = {
"Accept-Language": "en-US,en;q=0.5",
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
"Referer": "http://thewebsite.com",
"Connection": "keep-alive" 
}

def sendMessage(sock, message):
	sock.send("PRIVMSG #{} :{}\r\n".format(config.CHANNEL, message))	

def banUser(sock, user):
	sendMessage(sock, ".ban {}".format(user))

def timeout(sock, user, second = 500):
	sendMessage(sock, ".timeout {}".format(user, second))

def fillGuysList():
	while True:
		try:
			url = 'http://tmi.twitch.tv/group/user/deusetv/chatters'
			request = urllib2.Request(url, headers=REQUEST_HEADERS)
			response = urllib2.open(request).read()
			if response.find('502 bad gateway') == -1:
				config.guyslist.clear()
				data = json.loads(response)
				for i in data["chatters"]["moderators"]:
					config.guyslist[i] = "mod"
				for i in data["chatters"]["admins"]:
					config.guyslist[i] = "admins"
				for i in data["chatters"]["global_mods"]:
					config.guyslist[i] = "global_mod"
				for i in data["chatters"]["staff"]:
					config.guyslist[i] = "staff"

		except:
			'Sorry, but there is an unexpected error...'
	sleep(3)		

def userStatus(user):
	return user	in config.guyslist