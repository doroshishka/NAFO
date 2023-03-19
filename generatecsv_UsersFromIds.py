from datetime import datetime
from modules import tools
from modules import csv

fileName = "users.csv"


def main():
    global output_folder
    output_folder = ""
    folder = tools.get_command_folder()

    csv.generateUsersFromIds(folder, fileName)


if __name__ == "__main__":
    main()
