import tweepy
import facebook
import linkedin_v2
import schedule
import time
import os

# Configuration
TWITTER_API_KEY = os.getenv('TWITTER_API_KEY')
TWITTER_API_SECRET = os.getenv('TWITTER_API_SECRET')
TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
TWITTER_ACCESS_SECRET = os.getenv('TWITTER_ACCESS_SECRET')

FACEBOOK_ACCESS_TOKEN = os.getenv('FACEBOOK_ACCESS_TOKEN')
FACEBOOK_PAGE_ID = os.getenv('FACEBOOK_PAGE_ID')

LINKEDIN_ACCESS_TOKEN = os.getenv('LINKEDIN_ACCESS_TOKEN')

# Functions
def post_to_twitter(message):
    auth = tweepy.OAuth1UserHandler(
        TWITTER_API_KEY, TWITTER_API_SECRET,
        TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET
    )
    api = tweepy.API(auth)
    try:
        api.update_status(status=message)
        print("Posted to Twitter.")
    except Exception as e:
        print(f"Failed to post to Twitter: {e}")

def post_to_facebook(message):
    graph = facebook.GraphAPI(access_token=FACEBOOK_ACCESS_TOKEN)
    try:
        graph.put_object(parent_object=FACEBOOK_PAGE_ID, connection_name='feed', message=message)
        print("Posted to Facebook.")
    except Exception as e:
        print(f"Failed to post to Facebook: {e}")

def post_to_linkedin(message):
    headers = {
        'Authorization': f'Bearer {LINKEDIN_ACCESS_TOKEN}',
        'Content-Type': 'application/json',
        'X-Restli-Protocol-Version': '2.0.0'
    }
    payload = {
        "author": "urn:li:person:YOUR_PERSON_URN",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": message
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }
    try:
        response = requests.post('https://api.linkedin.com/v2/ugcPosts', headers=headers, json=payload)
        response.raise_for_status()
        print("Posted to LinkedIn.")
    except Exception as e:
        print(f"Failed to post to LinkedIn: {e}")

def post_update():
    message = "Automated post from Python Automation Script! #Automation #Python"
    post_to_twitter(message)
    post_to_facebook(message)
    post_to_linkedin(message)

# Schedule
schedule.every().day.at("09:00").do(post_update)

# Main Loop
if __name__ == "__main__":
    print("Social Media Automation Started.")
    while True:
        schedule.run_pending()
        time.sleep(60)  # wait one minute
