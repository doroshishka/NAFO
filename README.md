# NAFO
Collecting NAFO users on Twitter and their followings


# ----------------------------------
# General info
# ----------------------------------
# To check Python version
py --version
python --version
python3 --version

# To install pip
sudo apt install python3-pip

# To install a module
pip install modules
pip install pandas
...

# ----------------------------------
# Useful tips
# ----------------------------------
#Create output folder from the beginning in the same folder where the script is located

#Stop running the script from the terminal: ctrl+c

#if the process interrupts, then just put the last folder created as output, as in the examples below. Put the command in the terminal

#generate csv has to be called from the terminal

# ----------------------------------
# tweets by ids
# ----------------------------------
# To extract tweets
python .\tweetExtractor_Ids.py
# To resume extraction after failure in existing folder
python .\tweetExtractor_Ids.py "outputs_2023.03.07_22.31.54,684609"
# To generate CSV
python .\generatecsv_Ids.py "outputs/outputs_2023.03.07_21.51.28,329584"

# ----------------------------------
# tweets by keywords
# ----------------------------------
# To extract tweets
python .\tweetExtractor_Keywords.py
# To resume extraction after failure in existing folder
python .\tweetExtractor_Keywords.py "outputs_2023.03.07_21.55.18,352585"
# To generate CSV
python .\generatecsv_Keywords.py "outputs/outputs_2023.03.10_15.16.02,600495"

# ----------------------------------
# users by ids
# ----------------------------------
# To extract users
python .\userExtractor_Ids.py
# To resume extraction after failure in existing folder
python .\userExtractor_Ids.py "outputs_2023.03.07_21.56.10,054085"
# To generate CSV
python .\generatecsv_UsersFromIds.py "outputs/outputs_2023.03.07_21.56.10,054085"

# ----------------------------------
# Followers
# ----------------------------------
# To extract followers
python userFollowingExtractor_Ids.py
# To resume extraction after failure in existing folder
python userFollowingExtractor_Ids.py "outputs_2023.03.13_21.56.17,278701"
# To generate CSV - TO DO
