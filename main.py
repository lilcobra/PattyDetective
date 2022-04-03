from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

#check afl website to see if Pattrick Murtagh is playing

def getDriver(URL):
    driver = None
    try:
        driver = webdriver.Chrome()
    except:
        print("chrome driver outdated please go to https://sites.google.com/chromium.org/driver/ to download new version")
        exit()
    
    driver.get(URL)

    return driver

def closeDriver(driver):
    driver.close()

def checkPattyStatty():
    sauce = "https://www.afl.com.au/matches/team-lineups"
    driver = getDriver(sauce)

    games = driver.find_elements(by=By.CLASS_NAME, value="match-list-alt__item")

    #print(len(games))
    GCgame = []
    for game in games:
        homeTeam = game.find_element(by=By.CLASS_NAME, value="match-list-alt__header-team--home")
        awayTeam = game.find_element(by=By.CLASS_NAME, value="match-list-alt__header-team--away")
        if homeTeam.text == "Gold Coast Suns":
            GCgame.append(game)
            GCgame.append(True)
            break
        if awayTeam.text == "Gold Coast Suns":
            GCgame.append(game)
            GCgame.append(False)
            break

    if len(GCgame) == 0:
        closeDriver(driver)
        return "Patty is not Playing, Suns aren't playing this week."

    homeTeam = GCgame[0].find_element(by=By.CLASS_NAME, value="match-list-alt__header-team--home")
    awayTeam = GCgame[0].find_element(by=By.CLASS_NAME, value="match-list-alt__header-team--away")

    team = ""
    if GCgame[1]:
        team = awayTeam.text
        team += " at home!!!"
    else:
        team = homeTeam.text
        team += " away from home!!!"
    
    btn = GCgame[0].find_element(by=By.CLASS_NAME, value="js-expand-trigger")
    btn.click()

    #check lineups
    #check if EMG
    #also check if sub

    lineup = GCgame[0].find_element(by=By.CLASS_NAME, value="team-lineups__wrapper")
    players = lineup.text.split('\n')
    for i in range(len(players)):
        if players[i] == "[42] Patrick Murtagh," or players[i] == "[42] Patrick Murtagh":
            if i > 60:
                out = "Patty is listed as an emergency against " + team
                closeDriver(driver)
                return out
            else:
                out = "Holy sh!t, Patty is PLAYING against " + team
                closeDriver(driver)
                return out
    
    #check sub
    rows = GCgame[0].find_elements(by=By.CLASS_NAME, value="team-lineups__row")
    if len(rows) > 0:
        subs = (rows[-1].text).split('\n')
        if subs[0] == "Patrick Murtagh" or subs[2] == "Patrick Murtagh":
            if subs[1] == "SUB":
                out = "Patty is Playing as the medical against " + team
                closeDriver(driver)
                return out
            elif subs[1] != "OUT":
                out = "Okay something weird happened, but I think Patty is PLAYING against " + team
                closeDriver(driver)
                return out
    #time.sleep(5)
    closeDriver(driver)
    return "Patty is not Playing"

if __name__ == "__main__":
    print(checkPattyStatty())
    input("Press Enter... ")
