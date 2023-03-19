import csv
from datetime import datetime
from modules import tools
from modules import csv

fileName = "tweetreplies.csv"


def main():
    global output_folder
    output_folder = ""
    folder = tools.get_command_folder()

    csv.generate(folder, fileName)


if __name__ == "__main__":
    main()
