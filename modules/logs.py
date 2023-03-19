from datetime import datetime

output_folder = ""


def set_folder(folder):
    global output_folder
    output_folder = folder


def log(*message):
    global output_folder
    date_time = datetime.now().strftime("%H.%M.%S,%f")
    text = " {} - {}".format(date_time, ' '.join(message))
    print(text)
    if len(output_folder) > 0:
        with open("{}/{}".format(output_folder, "log.txt"), "a") as outfile:
            outfile.write(text + "\n")


def log_title(title):
    global output_folder
    log("")
    log("======================================================================")
    log(" {}".format(title))
    log("======================================================================")


def log_section(title):
    global output_folder
    log("")
    log(" {}".format(title))
    log("----------------------------------------------------------------------")


def get_date_time():
    global output_folder
    now = datetime.now()  # current date and time
    date_time = now.strftime("%Y.%m.%d_%H.%M.%S,%f")
    return date_time
