import requests
class twitchAPI:
    def __init__(self,clientID,clientSecret,channel):
        self.clientID = clientID
        self.clientSecret = clientSecret
        self.channel = channel                
        body = {
            'client_id': self.clientID,
            'client_secret': self.clientSecret,
            "grant_type": 'client_credentials'
            }
        r = requests.post('https://id.twitch.tv/oauth2/token', body)
        keys = r.json()
        self.headers = {
            'Client-ID': self.clientID,
            'Authorization': 'Bearer ' + keys['access_token']
                }

    def getInfoIfLive(self):
        stream = requests.get('https://api.twitch.tv/helix/streams?user_login=' + self.channel, headers=self.headers)
        stream_data = stream.json()
        info = {}
        if len(stream_data['data']) == 1:
            info["game"] = stream_data['data'][0]['game_name']
            info["viewers"] = stream_data['data'][0]['viewer_count']
        return info

    def checkLive(self):
        stream = requests.get('https://api.twitch.tv/helix/streams?user_login=' + self.channel, headers=self.headers)
        stream_data = stream.json()
        if len(stream_data['data']) == 1:
            return True
        else:
            return False

