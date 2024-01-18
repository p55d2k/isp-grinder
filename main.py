import os
import time

os.chdir(os.path.dirname(os.path.abspath(__file__)))

os.system("python3 -m pip install selenium")
print("\033c")

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
    teachers = feed.split("\n")
    if "" in teachers:
      teachers.remove("")
    if len(teachers) == 0:
      get_raw_input()
else:
  get_raw_input()

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

counts = [0]
currentindex = 0

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

for teacher in teachers:
  print("\033c")
  print("Getting " + teacher.upper() + "...\n")

  while True:
    cteacher = driver.find_element("xpath", '//*[@id="PageContent"]/table/tbody/tr/td[1]/table[1]/tbody/tr[3]/td/b[2]').text
    print("Attempt " + str(counts[currentindex] + 1) + " | Teacher: " + cteacher)

    if cteacher == teacher.upper():
      print("You got " + teacher.upper() + " in " + str(counts[currentindex]) + " tries!")

      if not os.path.exists("teachers/"):
        os.mkdir("teachers/")

      if not os.path.exists("teachers/" + teacher.lower() + '/'):
        os.mkdir("teachers/" + teacher.lower() + '/')

      img_element = driver.find_element("xpath", '//*[@id="PageContent"]/table/tbody/tr/td[1]/table[1]/tbody/tr[3]/td/img[1]')
      img_element.screenshot("teachers/" + teacher.lower() + "/" + teacher.lower() + ".png")

      if input("Do again? (y/n): ").lower().strip() == "y":
        currentindex += 1
        counts.append(0)
      else:
        with open("teachers/" + teacher.lower() + "/tries.txt", "a+") as f:
          f.write("tries took to get " + teacher.upper() + ": " + str(counts)[1:-1] + "\n")
          break
    else:
      counts[currentindex] += 1
    
    driver.refresh()
  
  counts = [0]

print("go check ur folder")
time.sleep(5)
