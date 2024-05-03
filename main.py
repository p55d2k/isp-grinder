import os
import time

os.chdir(os.path.dirname(os.path.abspath(__file__)))

print("\033c")
print("ISP-Grinder (Teacher Finder) v2.0 by @p55d2k")
print("DISCLAIMER: Do NOT use this tool for malicious purposes. This tool is intended for educational purposes only.")
time.sleep(2)

if os.path.exists("credentials.txt"):
    with open("credentials.txt", "r") as f:
        username = f.readline().strip()
        password = f.readline().strip()
else:
    username = input("Username: ")
    password = input("Password: ")
    print("\033c")

with open("credentials.txt", "w") as f:
    f.write(username + "\n")
    f.write(password + "\n")

teachers = []

def get_raw_input():
    global teachers
    teachers.append(input("Teacher name (full name): ").upper())

if os.path.exists("feed.txt"):
    with open("feed.txt", "r") as f:
        feed = f.read()
        raw_teachers = feed.split("\n")

        for teacher in raw_teachers:
            if teacher != "":
                teachers.append(teacher.upper())        

        for i in range(len(teachers)):
            teachers[i] = teachers[i].upper()

        if len(teachers) == 0:
            get_raw_input()
else:
    get_raw_input()
    
if not os.path.exists("teachers/"):
    os.mkdir("teachers/")

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

tries = 1

options = Options()
options.add_argument('--log-level=10')
driver = webdriver.Chrome(options=options)

driver.get("https://isphs.hci.edu.sg/")

driver.find_element("id", "txtUser").send_keys(username)
driver.find_element("id", "txtPassword").send_keys(password)

if driver.current_url == "https://isphs.hci.edu.sg/error700.asp":
    print("Invalid credentials")
    exit()

driver.find_element("xpath", '//*[@id="PageContent"]/form[1]/table/tbody/tr/td/table/tbody/tr/td/input[3]').click()

while len(teachers) > 0:
    cteacher = driver.find_element("xpath", '//*[@id="PageContent"]/table/tbody/tr/td[1]/table[1]/tbody/tr[3]/td/b[2]').text
    print("Attempt " + str(tries) + " | Teacher: " + cteacher)

    if cteacher in teachers:
        print("You got " + cteacher.upper() + " in " + str(tries) + " tries!")
            
        foldername = cteacher.lower().replace("/", "", -1)

        if not os.path.exists("teachers/" + foldername + '/'):
            os.mkdir("teachers/" + foldername + '/')

        if not os.path.exists("teachers/" + foldername + "/" + foldername + ".png"):
            img_element = driver.find_element("xpath", '//*[@id="PageContent"]/table/tbody/tr/td[1]/table[1]/tbody/tr[3]/td/img[1]')
            img_element.screenshot("teachers/" + foldername + "/" + foldername + ".png")

        with open("teachers/" + foldername + "/tries.txt", "a+") as f:
            f.write("Tries taken to get " + cteacher.upper() + ": " + str(tries)[1:-1] + "\n")
        
        teachers.remove(cteacher)
        
    tries += 1
    driver.refresh()

print("\033c")
print("ISP Teacher Finder has completed!")
time.sleep(5)
