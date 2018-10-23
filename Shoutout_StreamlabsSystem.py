import clr
import sys
import json
import os
import ctypes
import codecs
import time

ScriptName = "Scheduled Shoutouts"
Website = ""
Description = "Shoutouts on a timer"
Creator = "MrShojy"
Version = "0.1"

configFile = "config.json"
namesFile = "names.txt"
formatsFile = "formats.txt"
settings = {}
path = ""

namesList = []
formatsList = []
currentQuestion = ""
currentAnswers = []
currentReward = 0
namesLocation = ""
formatsLocation = ""

resetTime = 0


def ScriptToggled(state):
	return

def Init():
	global namesList, formatsList, settings, path, namesLocation, formatsLocation

	path = os.path.dirname(__file__)
	try:
		with codecs.open(os.path.join(path, configFile), encoding='utf-8-sig', mode='r') as file:
			settings = json.load(file, encoding='utf-8-sig')
	except:
		settings = {
			"liveOnly": True,
			"interval": 15,
			"apiKey": ""
		}

	namesLocation = os.path.join(path, namesFile)
	formatsLocation = os.path.join(path, formatsFile)

	LoadNames()
	LoadFormats()

	return

def LoadNames():
	global namesList, namesLocation
	try: 
		with codecs.open(namesLocation, encoding="utf-8-sig", mode="r") as file:
			namesList = [line.strip() for line in file]
	except:
		if os.path.isfile(namesLocation): 
			namesList = ["If you see this message save the file as UTF-8"]
		else: 
			with codecs.open(namesLocation, encoding="utf-8-sig", mode="w+") as file:
				file.write('MrShojy')
				namesList = [['MrShojy']]
	
	return

def LoadFormats():
	global formatsList, formatsLocation
	try: 
		with codecs.open(formatsLocation, encoding="utf-8-sig", mode="r") as file:
			formatsList = [line.strip() for line in file]
	except:
		if os.path.isfile(formatsLocation): 
			formatsList = ["If you see this message save the file as UTF-8"]
		else: 
			with codecs.open(formatsLocation, encoding="utf-8-sig", mode="w+") as file:
				file.write('$user is awesome! Check them out over at $url <3 They were last playing $game!')
				formatsList = [['$user is awesome! Check them out over at $url <3 They were last playing $game!']]

	return
def Execute(data):
	return

def ReloadSettings(jsonData):
	Init()
	return

def OpenReadMe():
	location = os.path.join(os.path.dirname(__file__), "README.txt")
	os.startfile(location)
	return

def OpenNamesFile():
	location = os.path.join(os.path.dirname(__file__), namesFile)
	os.startfile(location)
	return

def OpenFormatsFile():
	location = os.path.join(os.path.dirname(__file__), formatsFile)
	os.startfile(location)
	return


def Tick():
	
	global namesList, formatsList, resetTime, currentName, names

	if (settings["liveOnly"] and Parent.IsLive()) or (not settings["liveOnly"]):
		currentTime = time.time()

		if(currentTime >= resetTime):
			resetTime = currentTime + (settings["intervalTime"] * 60)
		
			latestGame = ""

			currentName = namesList.pop(Parent.GetRandom(0, len(namesList)))
			
			outputMessage = formatsList[Parent.GetRandom(0, len(formatsList))]
			headers = {"Client-ID": settings["apiKey"]}
			r = json.loads(Parent.GetRequest("https://api.twitch.tv/kraken/channels/" + currentName, headers))
			data = json.loads(r["response"])
			
			latestGame = data["game"]


			if len(namesList) == 0:
				try: 
					with codecs.open(namesLocation, encoding="utf-8-sig", mode="r") as file:
						namesList = [line.strip() for line in file]
				except:
					if os.path.isfile(namesLocation): 
						names = ["If you see this message save the file as UTF-8"]
					else: 
						with codecs.open(namesLocation, encoding="utf-8-sig", mode="w+") as file:
							file.write('MrShojy')
							names = [['MrShojy']]

			outputMessage = outputMessage.replace("$user", currentName)
			outputMessage = outputMessage.replace("$url", ("https://www.twitch.tv/" + currentName))
			outputMessage = outputMessage.replace("$game", latestGame)

			Parent.SendStreamMessage(outputMessage)
	return
