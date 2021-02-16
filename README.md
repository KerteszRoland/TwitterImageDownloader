# TwitterImageDownloader
This project is about downloading images from tweets. 
It uses Recent search ("The recent search endpoint allows you to programmatically access filtered public Tweets posted over the last week.").

To use the repo create Bearer_token.txt file and paste your token there or modify it for your own preference.
The main function is SaveImagesFromTwitterByHashtag(hashtag, user, dir)

hashtag: Search is based on this hashtag. It will search in tweet replies.
  example: Github
 
user: The search will find tweets with this author. 
  example: RolandKertesz
  
dir: Where the images will be saved.
