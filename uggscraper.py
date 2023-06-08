from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def getUGGdata():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--ignore-certificate-errors")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = webdriver.Chrome(options=options)
    driver.get('https://u.gg/lol/aram-tier-list')
    for scrolling in range(15):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    uggscrapeddata = driver.find_elements(by=By.CLASS_NAME, value="rt-tr-group") #value="rt-tbody altenative

    uggdict = {}

    for i in uggscrapeddata:
        uggchampdata = i.text.split("\n")
        refactoreduggdata = {
            #champ name
            uggchampdata[1] : {
                'Win rate': uggchampdata[3],
                'Pick rate': uggchampdata[4],
                'Games played': uggchampdata[5],
                'Rank': uggchampdata[0],
                'Tier': uggchampdata[2]
            }
        }
        uggdict.update(refactoreduggdata)
        #winratedata = {uggchampdata[1]:{'Win rate': uggchampdata[3],}}
        #uggdict.update(winratedata)
    return uggdict
