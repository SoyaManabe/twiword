import tweepy
CONSUMER_KEY = "2A4B2OxH7X42Mf7MKMLxYHmzR"
CONSUMER_SECLET = "AaCbWmfTkYX7Od5wMajsbxwIQf4DYNLwGl0aMJ22ssNjhxkzrx"
ACCESS_KEY = "862481526016978948-oxa8NaL5nQnJgR50Zy7jApWmw16A8lO"
ACCESS_SECRET = "De5XNWklujix6UISadeqrLqrqzGAOggF5fS4qpeJNEEK0"
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECLET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

def userImg(screenName):
    user = api.get_user(screenName)
    imgUrl = user.profile_image_url
    return imgUrl

"""
keys of get_user
id...twitterid(int)
id_str...twitterid(str)
name...accountname
screen_name...@sdffg


"""

def collect(screenName, list):
    lists = api.list_timeline(screenName, "twiword")
    i=0
    for l in lists:
        datas = {}
        datas['name'] = l.user.name
        datas['screen_name'] = l.user.screen_name
        datas['profile_image_url'] = l.user.profile_image_url
        datas['text'] = l.text
        list.append(datas)
        i += 1
        if i == 5:
            break
    return list

