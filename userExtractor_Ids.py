# https://towardsdatascience.com/mining-replies-to-tweets-a-walkthrough-9a936602c4d6
# https://developer.twitter.com/apitools/api?endpoint=/2/users&method=get

from re import sub
import os
from datetime import datetime
from urllib.error import HTTPError
import pandas as pd

from modules import twitterApi
from modules import logs
from modules import files
from modules import tools
from modules import csv

output_folder = ""


def main():
    global output_folder

    cmdFolder = tools.get_command_folder()

    # files.set_main_output_folder("ExtractUsers/outputs")
    files.set_main_output_folder("outputs")
    output_folder = files.generate_folder(cmdFolder)
    print("output_folder:", output_folder)
    logs.set_folder(output_folder)

    # allUserIds = [
    #     "1001429905526149120",
    #     "1002301864929419264",
    #     "1003710181887365120",
    #     "1006944678132903936"
    # ]
    # data = pd.read_csv("ExtractUsers/user_ids.csv")
    data = pd.read_csv("user_ids.csv")
    df = pd.DataFrame(data, columns=['id'])
    # , 'name', 'screen_name', 'created_at', 'location', 'following_count', 'followers_count', 'listed_count', 'tweet_count', 'url', 'description', 'FtF ratio'])
    df = df.reset_index()  # make sure indexes pair with number of rows
    allUserIds = []
    for index, row in df.iterrows():
        allUserIds.append("{}".format(row["id"]))
    # print(allUserIds)
    # quit()

    logs.log_title("Start...")

    # get tweets
    total_count = len(allUserIds)
    logs.log_section("Get users by Ids")

    current_total = 0
    n = 100
    page = 1
    userIdChunks = [allUserIds[i * n:(i + 1) * n] for i in range((len(allUserIds) + n - 1) // n)]
    for userIds in userIdChunks:
        # print(userIds)
        users = twitterApi.get_users(userIds)
        result_count = len(users["data"])
        current_total += result_count
        usersStr = tools.get_json_str(users)
        files.save_file(usersStr, "users-{}-{}.json".format(page, int(total_count / 100) + 1))
        logs.log("Retrieved users: {}/{}".format(current_total, total_count))
        logs.log()
        page += 1

    logs.log("{} users retrieved!".format(total_count))
    logs.log_title("...End!")


if __name__ == "__main__":
    main()
