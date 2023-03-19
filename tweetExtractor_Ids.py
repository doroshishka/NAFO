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

    tweetIds = [
        "1579600182450454531",
        "1580114398584053760",
        "1545625637448306688",
        "1538290525756866560",
        "1578646774516174848",
        "1544479807982936064",
        "1563851548643426304",
        "1579064793264459777"
    ]

    logs.log_title("Start...")

    # get tweets
    logs.log_section("Getting tweets")

    tweets = twitterApi.get_tweets(tweetIds)
    tweetsStr = tools.get_json_str(tweets)
    files.save_file(tweetsStr, "tweets.json")

    # loop through tweets
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
                logs.log(
                    "{} replies found for tweet {} at token [{}]".format(result_count, conversationId, current_token))

                repliesStr = tools.get_json_str(replies)

                # if current_token == "":
                #     subFolder = "tweet-{}".format(conversationId)
                #     files.generate_sub_folder(subFolder)
                # fileName = "{}\\tweet-{}-replies-{}.json".format(subFolder, conversationId, current_token)
                fileName = "tweet-{}-replies-{}.json".format(conversationId, current_token)
                files.save_file(repliesStr, fileName)

                # needUsers = False
                # if needUsers:
                #     allAuthorIds =[reply["author_id"] for reply in replies["data"]]
                #     # Remove duplicate
                #     authorIds = [*set(allAuthorIds)]
                #     n = 100 #The number of values in the `ids` query parameter list [101] is not between 1 and 100
                #     authorIdChunks = [authorIds[i * n:(i + 1) * n] for i in range((len(authorIds) + n - 1) // n )]
                #     i = 1
                #     for authorIdChunk in authorIdChunks:
                #         authors = twitterApi.get_users(authorIdChunk)
                #         logs.log("Processing authors chunk {}/{} of {}".format(i,len(authorIdChunks), n))
                #         #print(get_json_str(a))
                #         for user in authors["data"]:
                #             fileName = "{}\\user-{}.json".format(subFolder, user["id"])
                #             if os.path.exists(fileName):
                #                 logs.log("User file already exists: {}".format(fileName))
                #             else:
                #                 userStr = tools.get_json_str(user)
                #                 #userData = user["data"]
                #                 files.save_file(userStr, fileName)

                #         i+=1

                # repliesStr = get_json_str(replies)
                # if current_token == "":
                #     subFolder = "tweet-{}".format(conversationId)
                #     generate_sub_folder(subFolder)
                # fileName = "{}\\tweet-{}-replies-{}.json".format(subFolder, conversationId, current_token)
                # save_file(repliesStr, fileName)
                # #print(replies)
                # # loop through replies to get users
                # reply_count = 1
                # for reply in replies["data"]:
                #     logs.log("Analyzing reply {}/{}".format(reply_count,result_count))
                #     authorId = reply["author_id"]
                #     fileName = "{}\\user-{}.json".format(subFolder, authorId)
                #     if os.path.exists(fileName):
                #         logs.log("User file already exists: {}".format(fileName))
                #     else:
                #         user = get_user(authorId)
                #         userStr = get_json_str(user)
                #         #userData = user["data"]
                #         save_file(userStr, fileName)
                #     reply_count += 1

            if "next_token" in replies["meta"]:
                current_token = replies["meta"]["next_token"]
            else:
                current_token = ""
                break
            logs.log()

        logs.log("{} replies retrieved!".format(total_count))

    csvFileName = "tweetreplies-{}.csv".format(logs.get_date_time())
    csv.generate(output_folder, csvFileName)

    logs.log_title("...End!")


if __name__ == "__main__":
    main()
