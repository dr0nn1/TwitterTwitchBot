import configparser
import time
import tweepy
import subprocess


from Twitch import twitch

def start():
    time.sleep(90)
    print("Slept 90 sec, starts.")
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
        twitterClient = tweepy.Client(
            consumer_key=consumerKey,
            consumer_secret=consumerSecret,
            access_token=accessToken,
            access_token_secret=accessSecret
        )   
    except KeyboardInterrupt:
        exit("Ctrl + c, exiting")
    except:
        subprocess.Popen("/usr/bin/python3 -u  /home/pi/twitterTwitchBot/main.py > /home/pi/twitterTwitchBot/cronjob.log 2>&1",shell=True)
        exit("qutting, something did not work when getting keys")
    
    print("Checking online")
    while True:
        try:
            if twitchBot.checkLive():
                info = twitchBot.getInfoIfLive()
                if info["game"] != game:
                    #twitter her!
                    game = info["game"]
                    status= f'LIRIK is now playing {info["game"]} with {info["viewers"]} viewers! https://www.twitch.tv/lirik'
                    twitterClient.create_tweet(text=status)
                    print("updated status")
            else:
                game = ""

            time.sleep(60)
        except KeyboardInterrupt:
            exit("Ctrl + c, exiting")
        except:
            subprocess.Popen("/usr/bin/python3 -u  /home/pi/twitterTwitchBot/main.py > /home/pi/twitterTwitchBot/cronjob.log 2>&1",shell=True)
            exit("qutting, something did not work")
 
        


if __name__ == "__main__":
    print("Starting program")
    start()
