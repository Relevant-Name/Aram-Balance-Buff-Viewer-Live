from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import json
from slpp import slpp as lua
import uggscraper

class WikiClass():
    uggdict = uggscraper.getUGGdata()
    def __init__(self):
        self.wikitable = None

    @classmethod
    def getWikiTable(cls):
        wik = cls()
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--ignore-certificate-errors")
        options.add_experimental_option('excludeSwitches', ['enable-logging']) #more ignoring errors

        driver = webdriver.Chrome(options=options)
        driver.get('https://leagueoflegends.fandom.com/wiki/Module:ChampionData/data')

        wikitable = driver.find_element(by=By.CLASS_NAME, value="mw-parser-output")
        wikitable = wikitable.text.strip("\n -abcdefghijklmnopqrstuvwxyz/ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890()<>[]:\'_=,.%;") #reg = re.sub(".*return", "", wikitable_web.text, flags=re.DOTALL).rstrip("\n<pre>/- [Category:Lua]")
        wikitable = (lua.decode(wikitable))
        wikitable = json.dumps(wikitable, indent=4)
        wik.wikitable = json.loads(wikitable) #dict
        return wik

    def getBalanceBuff(self, champnamelist):
        if self.wikitable:
            for champion in champnamelist.keys():
                if champion in self.wikitable.keys():
                    aram_stats = self.wikitable[champion]['stats'].get('aram', 0)
                    champnamelist[champion]['Balance Buff'] = aram_stats
                else:
                    champnamelist[champion]['Balance Buff'] = 0
                if champion in self.uggdict:
                    win_rate = self.uggdict[champion]['Win rate']
                    champnamelist[champion]['win rate'] = win_rate
        return champnamelist

