import requests
import os
import subprocess
from bs4 import BeautifulSoup

# display the Terms of Use notice
response = subprocess.run(["zenity", "--question", "--text=Terms of Use: This program interacts with the system during automatic installation and does not collect any data except that which it needs. By using this program, you agree to these terms. Do you agree?", "--title=Terms of Use"], stdout=subprocess.PIPE)

# check if the user agreed to the Terms of Use
if response.stdout.decode("utf-8") == "True":
    # initialize feedback dictionary
    feedback = {}

    # handle user input
    while True:
        program_name = input("Enter the name of the program to install or type 'view feedback': ")

        # check if the user wants to view feedback
        if program_name == "view feedback":
            password = input("Enter the password: ")
            if password == "privatefeedback99!":
                # display feedback
                for program, comment in feedback.items():
                    print(program + ": " + comment)
            else:
                print("Invalid password.")
            continue

        # search for the program's download page
        search_url = "https://www.google.com/search?q=" + program_name + "download"
        response = requests.get(search_url)

        # parse the response to find the download link
        soup = BeautifulSoup(response.text, "html.parser")
        download_link = soup.find("a", {"class": "download-link"})["href"]

        # download the installer
        installer_path = program_name + "-installer.exe"
        with open(installer_path, "wb") as installer:
            installer.write(requests.get(download_link).content)

        # run the installer
        installer_process = subprocess.Popen([installer_path])

        # accept the license agreement if it exists
        while True:
            # check if the license agreement window exists
            try:
                license_agreement_window = subprocess.check_output(["windowtitle", installer_process.pid]).decode("utf-8")
            except subprocess.CalledProcessError:
                # the license agreement window does not exist, so continue
                break

            # accept the license agreement
            subprocess.run(["sendkey", "spc", license_agreement_window])
            subprocess.run(["sendkey", "ret", license_agreement_window])

        # click "Next" until the installation is complete
        while True:
            try:
                next_button_window = subprocess.check_output(["windowtitle", installer_process.pid]).decode("utf-8")
            except subprocess.CalledProcessError:
                # the "Next" button window does not exist, so the installation must be complete
                break

            # click the "Next" button
            subprocess.run(["sendkey", "ret", next_button_window])

        # open the program
        subprocess.run([program_name + ".exe"])

        # ask the user to rate their experience and add feedback
rating = input("Please rate your experience with the installation (1-5): ")
comment = input("Enter any additional comments: ")
feedback[program_name] = comment

