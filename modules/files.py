from datetime import datetime
import os
from modules import logs

output_top_folder = ""
output_folder = ""


def set_main_output_folder(folder):
    global output_top_folder
    output_top_folder = folder
    logs.log("Setting main output folder to: {}".format(output_top_folder))


def generate_folder(folder):
    global output_folder

    if len(output_top_folder) == 0:
        logs.log("Main output folder has not been set using 'set_main_output_folder'!")
        quit()

    if folder == "":
        now = datetime.now()  # current date and time
        date_time = now.strftime("%Y.%m.%d_%H.%M.%S,%f")
        output_f = "{}/outputs_{}".format(output_top_folder, date_time)
        if not os.path.exists(output_f):
            os.mkdir(output_f)
            logs.log("Create folder: {}".format(output_f))
    else:
        output_f = 'outputs/' + folder
        logs.log("Folder already exists: {}".format(output_f))
    output_folder = output_f
    return output_f


def generate_sub_folder(folder):
    global output_folder
    if folder != "":
        output_f = "{}/{}".format(output_folder, folder)
        if not os.path.exists(output_f):
            os.mkdir(output_f)
            logs.log("Create subfolder: {}".format(output_f))
    return output_f


def save_file(content, fileName, showFullPath=False):
    global output_folder
    filePath = "{}/{}".format(output_folder, fileName)
    logs.log("Saving file: {}".format(filePath if showFullPath else fileName))
    with open(filePath, "w") as outfile:
        outfile.write(content)
    return filePath
