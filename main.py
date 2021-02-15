import requests

IMAGES_DIR = "images/"


def GetBearerToken():
    bearer_token = "NOT LOADED"
    with open("Bearer_token.txt", "r") as file:
        bearer_token = file.readline()
    return bearer_token


BEARER_TOKEN = GetBearerToken()


def GetMediaUrlsByTweetId(tweet_id):
    tweet_fields = "expansions=attachments.media_keys&media.fields=url"
    ids = "ids="+tweet_id
    url = "https://api.twitter.com/2/tweets?{}&{}".format(ids, tweet_fields)
    json_response = SendGetRequest(url)
    return json_response


def GetTweetsByHashtag(hashtag, user_access):
    query = "%23"+hashtag
    if user_access != "all":
        query += " from:"+user_access
    query += " has:hashtags"
    tweet_fields = "tweet.fields=conversation_id"
    url = "https://api.twitter.com/2/tweets/search/recent?query={}&{}".format(query, tweet_fields)
    response_json = SendGetRequest(url)
    return response_json


def GetHeaders(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def SendGetRequest(url):
    headers = GetHeaders(BEARER_TOKEN)
    response = requests.request("GET", url, headers=headers)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def GetRootTweet(tweet):
    root_tweet_id = tweet["conversation_id"]
    root_tweet = GetMediaUrlsByTweetId(root_tweet_id)
    return root_tweet


def SaveImage(img_url, where):
    img = requests.get(img_url+"?format=jpg&name=large")
    img_name = img_url.split('/')[4]
    file = open(where+img_name, "wb")
    file.write(img.content)
    file.close()


def SaveImagesFromTwitterByHashtag(hashtag, user_access, save_dir):
    image_counter = 0
    reply_tweets = GetTweetsByHashtag(hashtag, user_access)
    try:
        for reply_tweet in reply_tweets["data"]:
            root_tweet = GetRootTweet(reply_tweet)
            try:
                for image in root_tweet["includes"]["media"]:
                    image_counter += 1
                    image_url = image["url"]
                    SaveImage(image_url, save_dir)
            except KeyError:
                print("This tweet ({}) doesn't contain an image".format(root_tweet["data"][0]["id"]))
    except KeyError:
        print("There isn't a reply with the hashtag: #{}".format(hashtag))
    return "-- Saved {} images --".format(image_counter)


#test print(SaveImagesFromTwitterByHashtag("tesla", "elonmusk", IMAGES_DIR))
