import cloudscraper
from bs4 import BeautifulSoup
import keyboard
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
import time

quizlet_link = input("Quizlet link for terms: ")
c_scraper = cloudscraper.create_scraper()
request = c_scraper.get(quizlet_link)

soup = BeautifulSoup(request.text, "html.parser")
quizlet_terms = soup.find_all("span", {"class": "TermText"})

terms = {
    "terms": [],
    "definitions": []
}

def find_definition(_term):
    current = 0
    for term_ in terms["terms"]:
        if term_ == _term:
            return terms["definitions"][current]
        current = current + 1
    return "Taylor u suck at coding L (error)"


current_term = 0
for term in quizlet_terms:
    if (current_term % 2) == 0:
        terms["terms"].append(term.text.strip())
    else:
        terms["definitions"].append(term.text.strip())
    current_term = current_term + 1

print(f"Terms found: {len(terms['terms'])} Definitions found: {len(terms['definitions'])}")

options = webdriver.ChromeOptions()
options.add_argument("--disable-extensions")
options.add_argument("--start-maximized")
options.add_argument("--profile-directory=Default")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install(), options=options)
driver.delete_all_cookies()
driver.get("https://www.gimkit.com/join/6221912170895b0023a6f018")

running = False

while True:
    if keyboard.is_pressed("i"):
        running = not running
    if not running:
        continue

    time.sleep(0.1)
    soup_driver = BeautifulSoup(driver.page_source, "html.parser")
    #sc-csuNZv eXjQkb - for assingments
    #sc-bAtgIc lniRIx - for reg games
    word = soup_driver.find("div", {"class": "sc-csuNZv eXjQkb"})
    for s in find_definition(word.text.strip()):
        keyboard.write(s)
    time.sleep(0.1)
    keyboard.press_and_release("ENTER")
    time.sleep(0.1)
    keyboard.press_and_release("ENTER")
    time.sleep(0.1)

