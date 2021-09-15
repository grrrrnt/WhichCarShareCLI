services = ['BlueSG', 'CarClub', 'GetGo', 'Shariot', 'TribeCar']

import datetime as dt
import json
from os import write
import strings

# Input parameters
from_location = ""
to_location = ""
start_time = dt.time()
day = -1
duration = 0
distance = 0

# Menu
EXIT = -1
MAIN_MENU = 0
DISTANCE = 1
DURATION = 2
RESULTS = 3
SETTINGS = 4
RESET_CONFIRM = 5

with open('user.json', 'r') as f:
    user = json.load(f)

def main():
    print(strings.setup['welcome'])
    curr_page = MAIN_MENU

    if (user['first_run']):
        setup_user()
    
    while True:
        print("=============================")
        if (curr_page == EXIT):
            print(strings.setup['farewell'])
            break
        if (curr_page == MAIN_MENU):
            print(strings.setup['main_menu'])
            curr_page = main_menu()
        elif (curr_page == DISTANCE):
            distance = input(strings.prompts['distance'])
            curr_page = DURATION
        elif (curr_page == DURATION):
            duration = input(strings.prompts['duration'])
            curr_page = RESULTS
        elif (curr_page == RESULTS):
            # TODO: Generate results here
            print("distance = {} km, duration = {} min\n".format(str(distance), str(duration)))
            input(strings.prompts['enter'])
            curr_page = MAIN_MENU
        elif (curr_page == SETTINGS):
            curr_page = settings()
        elif (curr_page == RESET_CONFIRM):
            print(strings.setup['reset_confirm'])
            curr_page = reset_confirm()
        else:
            print("Didn't recognise that...")

###########
## PAGES ##
###########

def main_menu():
    option = int(input(format_responses([strings.responses['plan_trip'], strings.responses['settings'], strings.responses['exit']])))
    if (option == 1):
        curr_page = DISTANCE
    elif (option == 2):
        curr_page = SETTINGS
    elif (option == 3):
        curr_page = EXIT
    return curr_page

def settings():
    print(generate_profile())
    print(strings.setup['change_settings'])
    option = int(input(format_responses([strings.responses['change_name'], strings.responses['change_memberships'], strings.responses['reset'], strings.responses['back'], strings.responses['exit']])))
    if (option == 1):
        update_name()
        write_to_config()
        print(strings.setup['completed'])
        curr_page = SETTINGS
    elif (option == 2):
        update_memberships()
        write_to_config()
        print(strings.setup['completed'])
        curr_page = SETTINGS
    elif (option == 3):
        curr_page = RESET_CONFIRM
    elif (option == 4):
        curr_page = MAIN_MENU
    elif (option == 5):
        curr_page = EXIT
    return curr_page

def reset_confirm():
    option = int(input(format_responses([strings.responses['yes'], strings.responses['no']])))
    if (option == 1):
        reset_user()
        print(strings.setup['completed'])
        curr_page = SETTINGS
    elif (option == 2):
        print(strings.setup['cancelled'])
        curr_page = SETTINGS
    return curr_page

##############
## SETTINGS ##
##############

def setup_user():
    print(strings.setup['first_run_welcome'])
    update_name()
    user['first_run'] = False
    print(generate_memberships())
    update_memberships()
    write_to_config()

def update_name():
    name = input(strings.prompts['name'])
    if (name != ""):
        user['name'] = name

def update_memberships():
    memberships = input(strings.prompts['memberships'])
    if (memberships != ""):
        memberships = list(map(int, memberships.split(' ')))
        for i, s in enumerate(services):
            user['member'][s] = (i+1) in memberships

def reset_user():
    user['name'] = "Guest"
    user['first_run'] = True
    for s in services:
        user['member'][s] = False
    write_to_config()

def write_to_config():
    with open('user.json', 'w') as f:
        json.dump(user, f)

###############
## UTILITIES ##
###############

def generate_profile():
    return "Here is your profile:\n"\
            "  Name:           {}\n"\
            "{}".format(user['name'], generate_memberships())

def generate_memberships():
    memberships_list = "  Memberships:\n"
    memberships = user['member']
    index = 1
    for k, v in memberships.items():
        service_membership = "    {}. {}".format(str(index), k).ljust(18)
        service_membership += "Yes" if v else "No"
        memberships_list += (service_membership + "\n")
        index += 1
    return memberships_list

def format_responses(responses):
    formatted = ""
    for i, r in enumerate(responses):
        formatted += "{}. {}\n".format(str(i+1), r)
    formatted += "\n{}".format(strings.prompts['choose'])
    return formatted

if __name__ == '__main__':
    main()