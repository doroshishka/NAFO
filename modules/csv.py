import csv
import os
import json
import pandas as pd
from modules import logs

columns = [
    'id',
    'name',
    'screen_name',
    'created_at',
    'location',
    'following_count',
    'followers_count',
    'listed_count',
    'tweet_count',
    'url',
    'description'
]


def generateUsers(folder, fileName):
    logs.log_section(" Generate csv - Starting...")

    if len(folder) == 0:
        logs.log("Folder is required!")
    else:
        # Get the list of all files and directories
        path = folder
        posts = pd.DataFrame(columns=columns)
        i = 0
        for f in os.scandir(path):
            if (
                    f.is_file() and
                    "tweets-count-" not in f.name and
                    "tweets-" in f.name
            ):
                # print("File: {} / {}".format(f.name, f.path))
                logs.log("File: {}".format(f.name))
                fileContent = open(f.path, encoding="utf8")
                fileJson = json.load(fileContent)
                # logs.log(fileJson["data"][0]["id"])
                # print(filejson)
                # tweetId = fileJson["data"][0]["conversation_id"]
                users = fileJson["includes"]["users"]
                for user in users:
                    new_row = pd.DataFrame({
                        'id': '="{}"'.format(user["id"]),
                        'name': [user["name"]],
                        'screen_name': user["username"],
                        'created_at': [user["created_at"]],
                        'location': user["location"] if "location" in user else "",
                        'following_count': user["public_metrics"]["following_count"],
                        'followers_count': user["public_metrics"]["followers_count"],
                        'listed_count': user["public_metrics"]["listed_count"],
                        'tweet_count': user["public_metrics"]["tweet_count"],
                        'url': user["url"] if "url" in user else "",
                        'description': [user["description"]]
                    })
                    i = i + 1
                    # posts = posts.append(new_row)
                    posts = pd.concat([posts, new_row])
                filePath = path + "/{}".format(fileName)
                if not os.path.exists(filePath):
                    posts.to_csv(filePath, index=False, header=True, quoting=csv.QUOTE_NONNUMERIC, escapechar="\\",
                                 line_terminator='\n')
                else:
                    posts.to_csv(filePath, index=False, header=False, quoting=csv.QUOTE_NONNUMERIC, escapechar="\\",
                                 line_terminator='\n', mode='a')
                posts.drop(posts.index, inplace=True)
        logs.log("Saved file: '{}'".format(fileName))

    logs.log_section("Generate csv - Done!")


def generateUsersFromIds(folder, fileName):
    logs.log_section("Generate csv - Starting...")

    if len(folder) == 0:
        logs.log("Folder is required!")
    else:
        # Get the list of all files and directories
        path = folder
        posts = pd.DataFrame(columns=columns)
        i = 0
        for f in os.scandir(path):
            if (
                    f.is_file() and
                    "users-" in f.name
            ):
                logs.log("File: {}".format(f.name))
                fileContent = open(f.path, encoding="utf8")
                fileJson = json.load(fileContent)
                users = fileJson["data"]
                for user in users:
                    new_row = pd.DataFrame({
                        'id': '="{}"'.format(user["id"]),
                        'name': [user["name"]],
                        'screen_name': user["username"],
                        'created_at': [user["created_at"]],
                        'location': user["location"] if "location" in user else "",
                        'following_count': user["public_metrics"]["following_count"],
                        'followers_count': user["public_metrics"]["followers_count"],
                        'listed_count': user["public_metrics"]["listed_count"],
                        'tweet_count': user["public_metrics"]["tweet_count"],
                        'url': user["url"] if "url" in user else "",
                        'description': [user["description"]]
                    })
                    i = i + 1
                    posts = pd.concat([posts, new_row])
                filePath = path + "/{}".format(fileName)
                if not os.path.exists(filePath):
                    posts.to_csv(filePath, index=False, header=True, quoting=csv.QUOTE_NONNUMERIC, escapechar="\\",
                                 line_terminator='\n')
                else:
                    posts.to_csv(filePath, index=False, header=False, quoting=csv.QUOTE_NONNUMERIC, escapechar="\\",
                                 line_terminator='\n', mode='a')
                posts.drop(posts.index, inplace=True)
        logs.log("Saved file: '{}'".format(fileName))

    logs.log_section("Generate csv - Done!")


def generate(folder, fileName):
    logs.log_section("Generate csv - Starting...")

    if len(folder) == 0:
        logs.log(" Folder is required!")
    else:
        # Get the list of all files and directories
        # path = "ExtractUsers\\outputs\\{}".format(folder)
        # path = "ExtractUsers\\outputs\\outputs_2022.10.17_07.14.24,981521"
        path = folder
        # dir_list = os.listdir(path)
        posts = pd.DataFrame(columns=columns)
        i = 0
        for f in os.scandir(path):
            if f.is_file() and "-replies-" in f.name:
                # print("File: {} / {}".format(f.name, f.path))
                logs.log("File: {}".format(f.name))
                fileContent = open(f.path, encoding="utf8")
                fileJson = json.load(fileContent)
                logs.log(fileJson["data"][0]["id"])
                # print(filejson)
                tweetId = fileJson["data"][0]["conversation_id"]
                users = fileJson["includes"]["users"]
                for user in users:
                    new_row = pd.DataFrame({
                        'tweetId': '="{}"'.format(tweetId),
                        'id': '="{}"'.format(user["id"]),
                        'name': [user["name"]],
                        'screen_name': user["username"],
                        'created_at': [user["created_at"]],
                        'location': user["location"] if "location" in user else "",
                        'following_count': user["public_metrics"]["following_count"],
                        'followers_count': user["public_metrics"]["followers_count"],
                        'url': user["url"] if "url" in user else "",
                        'description': [user["description"]]
                    })
                    i = i + 1
                    # posts = posts.append(new_row)
                    posts = pd.concat([posts, new_row])
        posts.to_csv(path + "/{}".format(fileName), index=False, header=True, quoting=csv.QUOTE_NONNUMERIC,
                     escapechar="\\", line_terminator='\n')
        logs.log("Saved file: '{}'".format(fileName))

    logs.log_section(" Generate csv - Done!")
