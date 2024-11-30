# Christian DeVore
# Account Manager Microservice (Microservice B) for To-do/Task-management app

import json
import random

PIPE = "./pipeB.txt"

ACCOUNT_DB = "user_login.json"

used_ids = []

#
# The main program that handles the account manager
#
def main():
    # Do the user's action (create an account or login)
    # Load up the JSON database first
    while(True):
        with open(ACCOUNT_DB, "r+") as acctdata:
            accounts = json.load(acctdata)
            with open(PIPE, "r+") as acct_file:
                # Read and split the account file pipe into an array with 2 elements: 
                # [create account or login, username, password]
                output = acct_file.read()
                if (output != "" and output.isnumeric() == False):
                    print("This runs")
                    new_acct_info = output.split()
                    option = new_acct_info[0] # "create" = Create an account, "login" = login
                    username = new_acct_info[1]
                    password = new_acct_info[2]

                    # CREATE A NEW ACCOUNT
                    if option == "create":
                        # Make sure the username has not already been chosen
                        if (username in accounts.keys()):
                            acct_file.seek(0)
                            acct_file.truncate()
                            acct_file.write("0")
                        else:
                            # Create new JSON object containing the user's information and insert it into the file
                            id_exists = True # Assume ID exists before moving verifying it doesn't
                            while (id_exists):
                                new_user_id = int(random.random() * 1000000)
                                if new_user_id not in used_ids:
                                    id_exists = False
                                    used_ids.append(new_user_id)

                            new_user = {
                                username: {
                                    password: {
                                        "user_id": new_user_id
                                    }
                                }
                            }
                            accounts.update(new_user)

                            # Replace the JSON with the updated JSON w/ new user data
                            acctdata.seek(0)
                            acctdata.truncate()
                            json.dump(accounts, acctdata, indent=4)
                            print("New account created!")

                            # Send back the new user id through the communication pipe
                            acct_file.seek(0)
                            acct_file.truncate()
                            acct_file.write(str(new_user_id))

                    elif option == "login":
                        # Check to see if the username and password entered match up with an account
                        user_id = 0
                        try:
                            user_id = accounts[username][password]["user_id"]
                        except KeyError:
                            print("Error: username or password not found")
                        acct_file.seek(0)
                        acct_file.truncate()
                        acct_file.write(str(user_id))


# Run the main program to start
main()