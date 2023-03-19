# https://towardsdatascience.com/mining-replies-to-tweets-a-walkthrough-9a936602c4d6
# https://developer.twitter.com/apitools/api?endpoint=/2/users&method=get

from re import sub
import os
from datetime import datetime
from urllib.error import HTTPError
import pandas as pd
import json
import os

from modules import twitterApi
from modules import logs
from modules import files
from modules import tools
from modules import status as modStatus

output_folder = ""


def main():
    global output_folder
    cmdFolder = tools.get_command_folder()

    # files.set_main_output_folder("ExtractUsers\\outputs")
    files.set_main_output_folder("outputs")
    output_folder = files.generate_folder(cmdFolder)
    print("output_folder:", output_folder)
    logs.set_folder(output_folder)

    # to get the current working directory
    directory = os.getcwd()
    print(directory)

    # data = pd.read_csv("ExtractUsers\\user_ids.csv")
    # data = pd.read_csv("..\\ExtractUsers\\user_ids.csv")
    data = pd.read_csv("users_ids_March_6.csv")
    df = pd.DataFrame(data, columns=['id'])
    # , 'name', 'screen_name', 'created_at', 'location', 'following_count', 'followers_count', 'listed_count', 'tweet_count', 'url', 'description', 'FtF ratio'])
    df = df.reset_index()  # make sure indexes pair with number of rows
    allUserIds = []
    for index, row in df.iterrows():
        allUserIds.append("{}".format(row["id"]))

    #  Check if file exists
    modStatus.set_folder(output_folder)
    status = modStatus.get_status({
        "current_token": "",
        "status": "InProgress",
        "userId": ""
        # "userId": "998582014814154752"
    })

    if len(status["userId"]) > 0:
        userId = status["userId"]
    else:
        userId = allUserIds[0]

    userIndex = allUserIds.index(userId)
    # print(len(allUserIds), index)
    totalUsers = len(allUserIds)
    allUserIds = allUserIds[userIndex:]
    # print(len(allUserIds))

    # quit()

    # allUserIds = [
    #     "1001429905526149120",
    #     "1002301864929419264",
    #     "1003710181887365120",
    #     "1006944678132903936"
    # ]

    logs.log_title("Start...")

    total_count = len(allUserIds)
    logs.log_section("Get following for {} users".format(total_count))

    current_total = 0
    full_total_count = 0
    page = 1

    # statusStr = tools.get_json_str(status)
    # logs.log(statusStr)

    if status["status"] != "InProgress":
        logs.log("Already done processing! Exiting.")
        quit()

    i = 0
    current_token = status["current_token"]
    for userId in allUserIds:
        status["userId"] = userId

        modStatus.save_status(status)

        current_total = 0
        total_count = 0

        logs.log_section("User {}/{} - {}".format(userIndex, totalUsers, userId))
        user = twitterApi.get_user(userId)
        userStr = tools.get_json_str(user)
        files.save_file(userStr, "user-{}.json".format(userId))

        if "data" in user:
            total_count = user["data"]["public_metrics"]["following_count"]
            logs.log("User {} is following {} users. Retreiving...".format(userId, total_count))
        else:
            logs.log("Error occured for User {}!".format(userId, total_count))

        while "data" in user:
            # while i < 3:
            i += 1
            # print(userIds)
            users = twitterApi.get_following(userId, current_token)
            if len(users) > 0 and "data" in users:
                result_count = len(users["data"])
                full_total_count += result_count
            else:
                result_count = 0

            if result_count == 0:
                logs.log("No following found for user {} at token [{}]".format(userId, current_token))
            else:
                logs.log(
                    "{} following users found for user {} at token [{}]".format(result_count, userId, current_token))
                current_total += result_count
                usersStr = tools.get_json_str(users)
                files.save_file(usersStr, "user-{}-following-users-{}.json".format(userId, current_token))
                logs.log("Retrieved following users: {}/{}".format(current_total, total_count))
                page += 1

            if "meta" in users and "next_token" in users["meta"]:
                current_token = users["meta"]["next_token"]
            else:
                current_token = ""
                break
            status["current_token"] = current_token

            logs.log()
        current_token = ""
        userIndex += 1

    logs.log("{} following users retrieved!".format(total_count))

    status["status"] = "Done"
    modStatus.save_status(status)

    logs.log_title("...End!")


if __name__ == "__main__":
    main()
