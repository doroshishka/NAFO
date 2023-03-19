import urllib.parse
from urllib.error import HTTPError
from modules import logs
import time
import requests
import json

# To set your enviornment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
# bearer_token = os.environ.get("BEARER_TOKEN")
bearer_token = "AAAAAAAAAAAAAAAAAAAAALk59wAAAAAAgj1yoGNdH73gW3Y96MRYA6%2BsAYw%3DClZ3UtNfjweAj0YC5fHIpjFuNuY7Ya5KFVn797FGpvJQBydHu6"

userFields = [
    "created_at",
    "description",
    "entities",
    "id",
    "location",
    "name",
    "pinned_tweet_id",
    "profile_image_url",
    "protected",
    "public_metrics",
    "url",
    "username",
    "verified",
    "withheld"
]

tweetFields = [
    "author_id",
    "conversation_id",
    "created_at",
    "in_reply_to_user_id"
]

twitterUrl = "https://api.twitter.com"


# def create_url_searchusers(keyword, page, count):
#     global twitterUrl
#     url = "{}/1.1/users/search.json".format(twitterUrl)
#     url = add_query_param(url, "page", page)
#     url = add_query_param(url, "count", count)
#     url = add_query_param(url, "q", keyword)
#     return url

def create_url_following(userid, next_token=""):
    global twitterUrl
    url = "{}/2/users/{}/following".format(twitterUrl, userid)
    url = add_query_param(url, "user.fields", ",".join(userFields))
    url = add_query_param(url, "pagination_token", next_token)
    url = add_query_param(url, "max_results", "1000")
    # url = add_query_param(url, "max_results", "5")
    return url


def create_url_gettweets(ids):
    global twitterUrl
    url = "{}/2/tweets".format(twitterUrl)
    url = add_query_param(url, "ids", ','.join(ids))
    url = add_query_param(url, "tweet.fields", ",".join(tweetFields))
    return url


def create_url_searchtweets(keywords, next_token=""):
    global twitterUrl
    url = "{}/2/tweets/search/all".format(twitterUrl)
    url = add_query_param(url, "query", urllib.parse.quote(' OR '.join(keywords)))
    url = add_query_param(url, "start_time", "2021-01-01T00:00:00.000Z")
    url = add_query_param(url, "tweet.fields", ",".join(tweetFields))
    url = add_query_param(url, "expansions", "author_id,in_reply_to_user_id,referenced_tweets.id")
    url = add_query_param(url, "user.fields", ",".join(userFields))
    url = add_query_param(url, "next_token", next_token)
    url = add_query_param(url, "max_results", "500")
    return url


def create_url_counttweets(keywords, next_token=""):
    global twitterUrl
    url = "{}/2/tweets/counts/all".format(twitterUrl)
    url = add_query_param(url, "query", urllib.parse.quote(' OR '.join(keywords)))
    url = add_query_param(url, "start_time", "2021-01-01T00:00:00.000Z")
    url = add_query_param(url, "granularity", "day")
    url = add_query_param(url, "next_token", next_token)
    return url


def create_url_replies(id, next_token):
    global twitterUrl
    url = "{}/2/tweets/search/all".format(twitterUrl)
    url = add_query_param(url, "query", "conversation_id:{}".format(id))
    url = add_query_param(url, "max_results", "500")
    url = add_query_param(url, "tweet.fields", ",".join(tweetFields))
    url = add_query_param(url, "expansions", "author_id,in_reply_to_user_id,referenced_tweets.id")
    url = add_query_param(url, "user.fields", ",".join(userFields))
    url = add_query_param(url, "next_token", next_token)
    return url


def create_url_getuser(id):
    global twitterUrl
    global userFields
    url = "{}/2/users/{}".format(twitterUrl, id)
    url = add_query_param(url, "user.fields", ",".join(userFields))
    return url


def create_url_getusers(ids):
    global twitterUrl
    global userFields
    url = "{}/2/users".format(twitterUrl)
    url = add_query_param(url, "ids", ','.join(ids))
    url = add_query_param(url, "user.fields", ",".join(userFields))
    return url


def add_query_param(url, param, value):
    newUrl = url
    if len(param) > 0 and len(value) > 0:
        op = "?" if "?" not in url else "&"
        # print(newUrl, op, param, value)
        newUrl += "{}{}={}".format(op, param, value)
    return newUrl


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2UserLookupPython"
    return r


def connect_to_endpoint(url):
    global output_folder
    retry = 0
    while retry < 20:
        response = requests.request("GET", url, auth=bearer_oauth, )
        # print(response.status_code)
        if (
                response.status_code == 429 or  # Rate Limit
                response.status_code == 503  # Serice Unavailable
        ):
            logs.log("Rate Limit: {} {}".format(response.status_code, response.text))
            retry += 1
            logs.log("Retrying in 60s - {}/20".format(retry, 3))
            time.sleep(60)
            # Exception: Request returned an error: 429 {"title":"Too Many Requests","detail":"Too Many Requests","type":"about:blank","status":429}
            # raise Exception(
            #     "Rate Limit: {} {}".format(
            #         response.status_code, response.text
            #     )
            # )
        else:
            break
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def get_following(userId, nextToken=""):
    global output_folder
    logs.log("Search following for userId: {} at token [{}]".format(userId, nextToken))
    url = create_url_following(userId, nextToken)
    json_response = connect_to_endpoint(url)
    if "meta" in json_response:
        result_count = json_response["meta"]["result_count"]
        logs.log("# Following retrieved: {}".format(result_count))
    else:
        logs.log("Error retrieving following for user id {}".format(userId))
    time.sleep(0.5 * 2)
    return json_response


def get_tweets(ids):
    global output_folder
    logs.log("Get tweets with ids: {} => {}...".format(len(ids), ids[:3]))
    url = create_url_gettweets(ids)
    json_response = connect_to_endpoint(url)
    time.sleep(0.5 * 2)
    return json_response


def search_tweets(keywords, nextToken=""):
    global output_folder
    logs.log("Search tweets with keywords: {} => {}... at token [{}]".format(len(keywords), keywords[:5], nextToken))
    url = create_url_searchtweets(keywords, nextToken)
    json_response = connect_to_endpoint(url)
    result_count = json_response["meta"]["result_count"]
    logs.log("# Tweets retrieved: {}".format(result_count))
    time.sleep(0.5 * 2)
    return json_response


def count_tweets(keywords, nextToken=""):
    global output_folder
    logs.log("Count tweets with keywords: {} => {}... at token [{}]".format(len(keywords), keywords[:5], nextToken))
    url = create_url_counttweets(keywords, nextToken)
    # logs.log("url", url)
    json_response = connect_to_endpoint(url)
    result_count = json_response["meta"]["total_tweet_count"]
    logs.log("# Tweets counted by month: {}".format(result_count))
    time.sleep(0.5 * 2)
    return json_response


def get_tweet_replies(id, current_token=""):
    global output_folder
    logs.log("Get tweet replies at token [{}]".format(current_token))
    url = create_url_replies(id, current_token)
    json_response = connect_to_endpoint(url)
    # print(url, json_response)
    # quit()
    time.sleep(0.5 * 2)
    return json_response


def get_user(id):
    global output_folder
    logs.log("Get user: {}".format(id))
    url = create_url_getuser(id)
    json_response = connect_to_endpoint(url)
    time.sleep(0.5 * 2)
    return json_response


def get_users(ids):
    global output_folder
    logs.log("Get users: {} - {}...".format(len(ids), ','.join(ids[:3])))
    url = create_url_getusers(ids)
    json_response = connect_to_endpoint(url)
    time.sleep(0.5 * 2)
    return json_response


# To refactor
def extract_following(output_folder, userId):
    url = create_url_following(userId)

    apiCallCount = 0
    try:
        # Catch Exception
        apiCallCount += 1
        json_response = connect_to_endpoint(url)
        followers = json.dumps(json_response, indent=4, sort_keys=True)

        fileName = "user-{}-followers.json".format(userId)
        logs.log("    - {}".format(fileName))
        with open("{}\{}".format(output_folder, fileName), "w") as outfile:
            # jsonfollowers = json.dumps(followers, indent=4)
            jsonfollowers = followers
            outfile.write(jsonfollowers)
    except:  # ValueError:
        fileName = "user-{}-followers-failed.json".format(userId)
        logs.log("     - {}".format(fileName))
        with open("{}\{}".format(output_folder, fileName), "w") as outfile:
            outfile.write("")
        raise IOError("Failed pulling following!")
