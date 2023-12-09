from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.remote.remote_connection import LOGGER
from selenium.common.exceptions import SessionNotCreatedException, TimeoutException
from time import sleep, localtime
import logging
import traceback
import sys, os
from random import choice
import requests
import json
import encodings.idna
import configparser

def getApiKey():
    config = configparser.ConfigParser()
    config.read("./settings.ini")
    return config['api']['jwt']

def getSearchPostNumber():
    config = configparser.ConfigParser()
    config.read("./settings.ini")
    return int(config['api']['search_post_number'])

def SettingBrowser(chromedriver_filepath, headless=True):
    option = webdriver.ChromeOptions()
    option.headless = headless
    ua = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17720', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19577', 'Chrome (AppleWebKit/537.1; Chrome50.0; Windows NT 6.3) AppleWebKit/537.36 (KHTML like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/530.6 (KHTML, like Gecko) Chrome/2.0.175.0 Safari/530.6', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246', 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/3.0.195.20 Safari/532.0', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14931', 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; en-US) AppleWebKit/532.2 (KHTML, like Gecko) Chrome/4.0.221.8 Safari/532.2', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17720', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586', 'Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/3.0.195.1 Safari/532.0', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/528.8 (KHTML, like Gecko) Chrome/1.0.156.0 Safari/528.8', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14931', 'Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/534.12 (KHTML, like Gecko) Chrome/9.0.579.0 Safari/534.12']
    user_ag = choice(ua)
    option.add_argument(f'user-agent={user_ag}')
    logging.debug(f'user_ag: {user_ag}')
    option.add_argument("--disable-blink-features=AutomationControlled")
    option.add_argument("window-size=1920x1080")
    option.add_argument("disable-infobars")
    option.add_argument("--disable-extensions")
    option.add_argument("--log-level=3")
    option.add_argument("--disable-popup-blocking")
    option.add_experimental_option("excludeSwitches", ["enable-automation"])
    option.add_experimental_option("useAutomationExtension", False)
    dc = DesiredCapabilities.CHROME
    dc['pageLoadStrategy'] = 'none'
    dc['loggingPrefs'] = {'driver': 'OFF', 'server': 'OFF', 'browser': 'OFF'}

    try:
        browser = webdriver.Chrome(chromedriver_filepath, options=option, desired_capabilities=dc)
    except SessionNotCreatedException:
        for _ in range(3):
            logging.error("''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''")
        logging.error("크롬 버전이 chromedriver.exe의 버전과 맞지 않습니다")
        logging.error("현재 크롬 버전을 확인 후에 버전에 맞는 chromedriver.exe를 다운받아주세요")
        for _ in range(3):
            logging.error("''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''")
        os.system('pause')
        sys.exit()
    browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined   
                }) 
                """
    })
    browser.maximize_window()

    url = "https://www.inven.co.kr/board/lostark/5355"
    browser.get(url)

    return browser

def GetSameGroupCharacterList(character_name) -> list:
    logging.debug(f"GetSameGroupCharacterList({character_name})")
    same_group_charactername_list = []
    if character_name == "":
        return same_group_charactername_list
    jwt = "bearer " + getApiKey()
    headers = {
        'accept': 'application/json',
        'authorization': jwt
    }
    url = f"https://developer-lostark.game.onstove.com/characters/{character_name}/siblings"
    response = requests.get(url, headers=headers)
    logging.debug(f"response.status_code: {response.status_code}")
    if response.status_code == 200 and response.json() is not None:
        for character in response.json():
            character_level = float("".join(character["ItemAvgLevel"].split(",")))
            if character_level >= 1445.0:
                same_group_charactername_list.append(character["CharacterName"])
        logging.debug(f"same_group_charactername_list: {same_group_charactername_list}")
        logging.info(f"캐릭터 닉네임: {character_name} 의 같은 원정대 캐릭터\n--> {same_group_charactername_list}")
        return same_group_charactername_list
    elif response.status_code == 429:
        logging.info("Throttling, RateLimit-Limit")
        return same_group_charactername_list
    else:
        logging.info("null")
        return same_group_charactername_list

def SearchInven(browser, character: str) -> list:
    logging.debug(f"SearchInven, args: {character}")
    logging.info(f"캐릭터 닉네임: {character} 검색 시작")
    ret_list = []
    browser.get("https://www.inven.co.kr/board/lostark/5355")
    if character == "":
        return ret_list
    try:
        WebDriverWait(browser, 5).until(ec.presence_of_element_located((By.ID, 'sword')))
    except TimeoutException:
        browser.get("https://www.inven.co.kr/board/lostark/5355")
        WebDriverWait(browser, 5).until(ec.presence_of_element_located((By.ID, 'sword')))
    browser.find_element_by_id("sword").clear()
    browser.find_element_by_id("sword").send_keys(character)
    browser.find_element_by_xpath('//*[@id="new-board"]/div[6]/form/button').click()
    for next_search in range(0, getSearchPostNumber()-1):
        try:
            WebDriverWait(browser, 5).until(ec.presence_of_element_located((By.XPATH, '//*[@id="new-board"]/form/div/table/tbody/tr')))
        except TimeoutException:
            logging.info("Timeout, site error")
            return ret_list
        rows = browser.find_elements_by_xpath('//*[@id="new-board"]/form/div/table/tbody/tr')
        if len(browser.find_elements_by_class_name("no-result")) != 0:
            continue
        for i in range(1, len(rows)):
            post = rows[i].find_element_by_class_name("subject-link")
            link = post.get_attribute("href")
            title = post.text
            ret_list.append((link, title))
        browser.find_element_by_css_selector('#new-board > div.board-bottom > div > button').click()
    logging.info(f"캐릭터 닉네임: {character} 검색 기록\n--> {ret_list}")
    return ret_list

def Search(browser, character_name: str):
    ret_list = []
    same_group_character_list = GetSameGroupCharacterList(character_name)
    for character in same_group_character_list:
        posts = SearchInven(browser, character)
        for post in posts:
            ret_list.append(post)
    return ret_list

