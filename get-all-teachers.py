import os
import time

os.chdir(os.path.dirname(os.path.abspath(__file__)))

print("\033c")
print("Get All Teachers | ISP-Grinder (Teacher Finder) v2.0 by @p55d2k")
print("Use Ctrl/Cmd + C to stop the program.")
print("DISCLAIMER: Do NOT use this tool for malicious/stalking purposes. This tool is intended for educational purposes only.\n")
time.sleep(1)

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

while True:
    try:
        cteacher = driver.find_element("xpath", '//*[@id="PageContent"]/table/tbody/tr/td[1]/table[1]/tbody/tr[3]/td/b[2]').text
    except:
        tries += 1
        driver.refresh()
        continue        

    print("Attempt " + str(tries) + " | Teacher: " + cteacher)
    
    if cteacher.lower() in ["system", "teacher01", "teacher02"]:
        tries += 1
        driver.refresh()
        continue
        
    foldername = cteacher.lower().replace("/", "", -1)

    # already exists
    if os.path.exists("teachers/" + foldername + '/'):
        with open("teachers/" + foldername + "/tries.txt", "a+") as f:
            f.write("Tries taken to get " + cteacher.upper() + ": " + str(tries)[1:-1] + "\n")
    else: # doesnt alr exist
        os.mkdir("teachers/" + foldername + '/')

        img_element = driver.find_element("xpath", '//*[@id="PageContent"]/table/tbody/tr/td[1]/table[1]/tbody/tr[3]/td/img[1]')
        img_element.screenshot("teachers/" + foldername + "/" + foldername + ".png")

        with open("teachers/" + foldername + "/tries.txt", "a+") as f:
            f.write("Tries taken to get " + cteacher.upper() + ": " + str(tries)[1:-1] + "\n")
        
    tries += 1
    driver.refresh()
