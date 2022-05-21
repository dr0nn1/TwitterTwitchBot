import configparser
import time
import tweepy

from Twitch import twitch

def start():
    print("Starting")
    time.sleep(90)
    consumerKey = ""
    consumerSecret = ""
    accessToken = ""
    accessSecret = ""

    clientID = ""
    clientSecret = ""
    config = configparser.ConfigParser()
    config.read("/home/pi/twitterTwitchBot/config.txt")
    config.sections()
    for key in config["Twitter"]:
        if key == "consumer-key":
            consumerKey = config.get("Twitter",key)
        if key == "consumer-secret":
            consumerSecret = config.get("Twitter",key)
        if key == "access-token":
            accessToken = config.get("Twitter",key)
        if key == "access-secret":
            accessSecret = config.get("Twitter",key)

    for key in config["Twitch"]:
        if key == "client-id":
            clientID = config.get("Twitch",key)
        if key == "client-secret":
            clientSecret = config.get("Twitch",key)
    
    game = ""
    try:
        twitchBot = twitch.twitchAPI(clientID,clientSecret,"lirik")
        auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
        auth.set_access_token(accessToken, accessSecret)
        api = tweepy.API(auth)
    except:
        exit("qutting, something did not work")
    
    while True:
        if twitchBot.checkLive():
            info = twitchBot.getInfoIfLive()
            if info["game"] != game:
                #twitter her!
                game = info["game"]
                status= f'@LIRIK is now playing {info["game"]} with {info["viewers"]} viewers!'
                api.update_status(status)
                print("updated status")
        else:
            game = ""
 
        time.sleep(60)


if __name__ == "__main__":
    start()
