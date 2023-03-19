# https://towardsdatascience.com/mining-replies-to-tweets-a-walkthrough-9a936602c4d6
# https://developer.twitter.com/apitools/api?endpoint=/2/users&method=get

from re import sub
import os
from datetime import datetime
from urllib.error import HTTPError

from modules import twitterApi
from modules import logs
from modules import files
from modules import tools
from modules import csv

output_folder = ""


def main():
    global output_folder

    cmdFolder = tools.get_command_folder()

    files.set_main_output_folder("outputs")
    output_folder = files.generate_folder(cmdFolder)
    print("output_folder:", output_folder)
    logs.set_folder(output_folder)

    keywords = [
        "NAFOarticle5",
        "WeAreNAFO",
        "fellarequest"
    ]

    logs.log_title("Start...")

    # get tweets
    logs.log_section("Searching tweets by keywords: {}".format(",".join(keywords)))

    current_token = ""
    current_total = 0
    while True:
        json_response = twitterApi.count_tweets(keywords, current_token)
        total_count = json_response["meta"]["total_tweet_count"]
        current_total += total_count
        tweetCountStr = tools.get_json_str(json_response)
        files.save_file(tweetCountStr, "tweets-count-{}.json".format(current_token))
        logs.log("Current Total {}".format(current_total))
        logs.log()
        if "next_token" in json_response["meta"]:
            current_token = json_response["meta"]["next_token"]
        else:
            current_token = ""
        if current_token == "" or total_count == 0:
            break
    logs.log("Final Total {}".format(current_total))
    logs.log()

    current_token = ""
    total_count = current_total
    current_total = 0
    pullReplies = False
    while True:
        # while False:
        tweets = twitterApi.search_tweets(keywords, current_token)
        result_count = int(tweets["meta"]["result_count"])
        current_total += result_count
        tweetsStr = tools.get_json_str(tweets)
        files.save_file(tweetsStr, "tweets-{}.json".format(current_token))

        logs.log("Retrieved tweets: {}/{}".format(current_total, total_count))

        # loop through tweets
        if pullReplies:
            for tweet in tweets["data"]:
                conversationId = tweet["conversation_id"]

                logs.log_section("Extracting replies for tweet {}".format(conversationId))

                # Page through the replies
                current_token = ""
                total_count = 0
                while True:
                    # Get replies
                    replies = twitterApi.get_tweet_replies(conversationId, current_token)
                    result_count = replies["meta"]["result_count"]
                    total_count += result_count
                    if result_count == 0:
                        logs.log("No reply found for tweet {} at token [{}]".format(conversationId, current_token))
                    else:
                        logs.log("{} replies found for tweet {} at token [{}]".format(result_count, conversationId,
                                                                                      current_token))
                        repliesStr = tools.get_json_str(replies)
                        fileName = "tweet-{}-replies-{}.json".format(conversationId, current_token)
                        files.save_file(repliesStr, fileName)

                    if "next_token" in replies["meta"]:
                        current_token = replies["meta"]["next_token"]
                    else:
                        current_token = ""
                        break
                    logs.log()

        logs.log("{} replies retrieved!".format(total_count))
        if "next_token" in tweets["meta"]:
            current_token = tweets["meta"]["next_token"]
        else:
            current_token = ""
        if current_token == "":
            break
        logs.log()

    if pullReplies:
        csvFileName = "tweetreplies-{}.csv".format(logs.get_date_time())
        csv.generate(output_folder, csvFileName)

    logs.log_title("...End!")


if __name__ == "__main__":
    main()
