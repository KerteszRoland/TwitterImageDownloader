import requests

IMAGES_DIR = "images/"


def GetBearerToken():
    bearer_token = "NOT LOADED"
    with open("Bearer_token.txt", "r") as file:
        bearer_token = file.readline()
    return bearer_token


BEARER_TOKEN = GetBearerToken()


def GetTweetWithMediaById(tweet_id):
    tweet_fields = "expansions=attachments.media_keys&media.fields=url"
    ids = "ids="+tweet_id
    url = "https://api.twitter.com/2/tweets?{}&{}".format(ids, tweet_fields)
    json_response = SendGetRequest(url)
    return json_response


def GetTweetsByHashtag(hashtag, user_access, quantity=10, plus_query=""):
    query = "%23"+hashtag+" "+plus_query
    if user_access != "all":
        query += " from:"+user_access
    tweet_fields = "tweet.fields=conversation_id"
    max_results = "max_results={}".format(quantity)
    url = "https://api.twitter.com/2/tweets/search/recent?query={}&{}&{}".format(query, tweet_fields, max_results)
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


def GetRootTweetId(tweet):
    root_tweet_id = tweet["conversation_id"]
    return root_tweet_id


def SaveImage(img_url, where):
    img = requests.get(img_url+"?format=jpg&name=large")
    img_name = img_url.split('/')[4]
    file = open(where+img_name, "wb")
    file.write(img.content)
    file.close()


def SaveImagesFromTwitterByHashtag(hashtag, user_access, quantity, save_dir):
    image_counter = 0
    reply_tweets = GetTweetsByHashtag(hashtag, user_access, quantity)
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


def Test(hashtag, user_access, quantity, save_dir):
    image_counter = 0
    plus_query = "has:images -is:retweet -has:videos -is:reply"
    tweets = GetTweetsByHashtag(hashtag, user_access, quantity, plus_query)
    for tweet in tweets["data"]:
        tweet_with_media = GetTweetWithMediaById(tweet["conversation_id"])
        try:
            for image in tweet_with_media["includes"]["media"]:
                image_counter += 1
                image_url = image["url"]
                SaveImage(image_url, save_dir)
        except:
            print(tweet_with_media)
            print("something went wrong")
    return "-- Saved {} images --".format(image_counter)

print(Test("model3", "all", 100, IMAGES_DIR))
#print(GetTweetsByHashtag("tesla", "RolandKertesz", 100))
#print(SaveImagesFromTwitterByHashtag("tesla", "all", 100, IMAGES_DIR))
