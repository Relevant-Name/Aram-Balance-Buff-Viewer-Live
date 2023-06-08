import subprocess
import re
import requests
import urllib3
import base64
import json

import wikiscraper
from wikiscraper import WikiClass

#
# Main logic file
# Contains functions for setting up the league client session connection,
# sorts out current champion info, and uses functions from the scrapers
# to get the needed data
#

class LeagueClient():
    wikidata = WikiClass.getWikiTable()

    def __init__(self):
        self.port = None
        self.password = None
        self.lapiheaders = None
        self.session = None
        self.response = None
        self.respSaved = None

        self.ChampList = []
        self.ChampListBench = []

    @classmethod
    def initalizeClient(cls):
        lcv = cls()
        try:
            command = "WMIC PROCESS WHERE name='LeagueClientUx.exe' GET commandline"
            output = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True).stdout.read().decode('utf-8')

            lcv.port = re.findall(r'"--app-port=(.*?)"', output)[0]
            lcv.password = re.findall(r'"--remoting-auth-token=(.*?)"', output)[0]
            userauth = base64.urlsafe_b64encode(f"riot:{lcv.password}".encode('UTF-8')).decode('ascii')
            userauth2 = (f"Basic {userauth}")
            lcv.lapiheaders = {"Authorization":userauth2, "Accept":"application/json"}

            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) # Disable the annoying certificate error
            lcv.session = requests.session()
            lcv.session.verify = False
            print(f"port - {lcv.port}, pass - {lcv.password}")
        except Exception as e:
            print("it probably isn't even open, error: ", e)
            return lcv
        return lcv

    def getChampSelectSession(self):
        try:
            r = self.session.get(f"https://127.0.0.1:{self.port}/lol-champ-select/v1/session", headers=self.lapiheaders)
            if r.status_code == 200:
                self.response = r.json()
                print("getChampSelectSession success!")
            elif r.status_code == 404:
                self.clearChampList()
                print("getChampSelectSession failed, Error 404 not in champ select probably, clearing champ list")
                return 200
        except Exception as e:
            self.__dict__.update(self.__class__.initalizeClient().__dict__)
            print("getChampSelectSession failed, Probably isn't open. Attempting to initalize client error:", e)

    def updateNumberList(self, sessionjson):
        #ClientChampSelectInfo = self.session.get(f"https://127.0.0.1:{self.port}/lol-champ-select/v1/session", headers=self.lapiheaders) #/lol-champ-select/v1/session #has "benchChampionIds": ,,,  "myTeam": [ {"championId": 0,}
        ClientChampSelectInfo = sessionjson
        for champion_data in ClientChampSelectInfo['myTeam']:
            self.ChampList.append(champion_data['championId'])
        if ClientChampSelectInfo['benchChampions']:
            for index, champ_name in enumerate(ClientChampSelectInfo['benchChampions']):
                champ_number = champ_name['championId']
                self.ChampListBench.append(champ_number)
        print("huge", self.ChampList, self.ChampListBench)

    def testdifferentendpoints(self):
        respon = self.session.get(f"https://127.0.0.1:{self.port}/lol-gameflow/v1/session", headers=self.lapiheaders)
        respon2 = self.session.get(f"https://127.0.0.1:{self.port}/liveclientdata/allgamedata", headers=self.lapiheaders)
        print("=============== lol-gameflow/v1/session data =================")
        print(respon.json())
        print("=============== liveclientdata/allgamedata =================")
        print(respon2.json())
        #return respon.json()

    def doEverythingLive(self):
        self.getChampSelectSession()

        if self.respSaved != self.response:
            try:
                self.clearChampList()
                self.updateNumberList(self.response)
                self.respSaved = self.response
            except Exception as e:
                print(e)
                self.clearChampList()
                self.respSaved = self.response
            else:
                who = getChampName(self.ChampList)
                whobench = getChampName(self.ChampListBench)
                balacedatateam = LeagueClient.wikidata.getBalanceBuff(who)
                balacedatabench = LeagueClient.wikidata.getBalanceBuff(whobench)
                buffboth = {"team":balacedatateam,"bench":balacedatabench}
                return buffboth

    def offlinetheory(self):
        self.updateNumberList(offlinetestdata)
        #whodict = {"team":getChampName(self.ChampNumList),"bench":getChampName(self.ChampNumListBench)}
        who = getChampName(self.ChampList)
        whobench = getChampName(self.ChampListBench)
        balacedatateam = LeagueClient.wikidata.getBalanceBuff(who)
        balacedatabench = LeagueClient.wikidata.getBalanceBuff(whobench)
        buffboth = {"team":balacedatateam,"bench":balacedatabench}
        return buffboth

    def clearChampList(self):
        self.ChampList = []
        self.ChampListBench = []
        self.CNumLstSaved = ['lol']
    def testCurrentlyLoggedIn(self):
        respon = self.session.get(f"https://127.0.0.1:{self.port}/lol-summoner/v1/current-summoner", headers=self.lapiheaders)
        print(respon.json())
        return respon.json()

#################################

class DDragonData():
    def __init__(self):
        self.ddragondata = requests.get("http://ddragon.leagueoflegends.com/cdn/13.3.1/data/en_US/champion.json").json()['data']
        self.champion_keys_to_names = {}
        self.champion_names_to_keys = {}
    @classmethod
    def getChampNumberList(cls):
        ckn = cls()
        for champion, info in ckn.ddragondata.items():
            ckn.champion_keys_to_names[info['key']] = info['name']
            ckn.champion_names_to_keys[info['name']] = info['key']
        return ckn

def getChampName(champid):
    champion_id_as_str = [str(x) for x in champid]
    champ_dict = {}

    for key, champ in dd.champion_keys_to_names.items():
        if key in champion_id_as_str:
            url = f"https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/champion-icons/{key}.png"
            champ_dict[champ] = {"Icon": url}
    return champ_dict

dd = DDragonData.getChampNumberList()
#savetable = WikiClass()
#savetable = WikiClass.getWikiTable()
lct = LeagueClient.initalizeClient()
#lct.testdifferentendpoints()
#print(lct.doeverythinglive())

#print(lct.getChampSelectSession())
#lct.offlinetheory()

try:
    with open('benchchampsession.json') as user_file:
        offlinetestdata = json.load(user_file)
except Exception as e:
    print("debug file not located", e)
#print(intheory(offlinetestdata))

def intheory(thedata):
    lct.updateNumberList(thedata)
    #lc.ChampNumList has champ numbers, need to find champ names
    who = getChampName(lct.ChampList)#has chammp names, now need to get balance buff data
    balancedatas = savetable.getBalanceBuff(who)
    return balancedatas

#/lol-lobby-team-builder/champ-select/v1/session event


