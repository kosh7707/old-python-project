from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.remote.remote_connection import LOGGER
from selenium.common.exceptions import SessionNotCreatedException, TimeoutException, JavascriptException, ElementNotInteractableException
from time import sleep, localtime
import traceback
import sys, os
from random import choice
from smsauth import SmsAuth
import encodings.idna

today_month = localtime().tm_mon
alert_waiting_t = 5

def SettingBrowser(chromedriver_filepath, headless=True):
    option = webdriver.ChromeOptions()
    option.headless = headless
    ua = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17720', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19577', 'Chrome (AppleWebKit/537.1; Chrome50.0; Windows NT 6.3) AppleWebKit/537.36 (KHTML like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/530.6 (KHTML, like Gecko) Chrome/2.0.175.0 Safari/530.6', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246', 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/3.0.195.20 Safari/532.0', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14931', 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; en-US) AppleWebKit/532.2 (KHTML, like Gecko) Chrome/4.0.221.8 Safari/532.2', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17720', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586', 'Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/3.0.195.1 Safari/532.0', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/528.8 (KHTML, like Gecko) Chrome/1.0.156.0 Safari/528.8', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14931', 'Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/534.12 (KHTML, like Gecko) Chrome/9.0.579.0 Safari/534.12']
    user_ag = choice(ua)
    option.add_argument(f'user-agent={user_ag}')
    option.add_argument("--disable-blink-features=AutomationControlled")
    option.add_argument("window-size=1920x1080")
    option.add_argument("disable-infobars")
    option.add_argument("--disable-extensions")
    option.add_argument("--log-level=3")
    option.add_argument("--disable-popup-blocking")
    # prefs = {'profile.default_content_setting_values': {'plugins': 2, 'popups': 2,
    #                                                     'geolocation': 2, 'notifications': 2,
    #                                                     'auto_select_certificate': 2, 'fullscreen': 2, 'mouselock': 2,
    #                                                     'mixed_script': 2, 'media_stream': 2, 'media_stream_mic': 2,
    #                                                     'media_stream_camera': 2, 'protocol_handlers': 2,
    #                                                     'ppapi_broker': 2, 'automatic_downloads': 2, 'midi_sysex': 2,
    #                                                     'push_messaging': 2, 'ssl_cert_decisions': 2,
    #                                                     'metro_switch_to_desktop': 2, 'protected_media_identifier': 2,
    #                                                     'app_banner': 2, 'site_engagement': 2, 'durable_storage': 2}}
    # option.add_experimental_option('prefs', prefs)
    option.add_experimental_option("excludeSwitches", ["enable-automation"])
    option.add_experimental_option("useAutomationExtension", False)
    dc = DesiredCapabilities.CHROME
    dc['pageLoadStrategy'] = 'none'
    dc['loggingPrefs'] = {'driver': 'OFF', 'server': 'OFF', 'browser': 'OFF'}

    try:
        browser = webdriver.Chrome(chromedriver_filepath, options=option, desired_capabilities=dc)
    except SessionNotCreatedException:
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

    url = "www.naver.com"
    browser.get(url)

    return browser

def Login(browser, id, pw):     # 로그인 성공 시 True, 아닐 시 False
    xp = "//*[@id='cyberId']"
    try:
        WebDriverWait(browser, 3).until(ec.presence_of_element_located((By.XPATH, xp)))
    except:
        xp = '//*[@id="mainBody"]/div/div[2]/div/fieldset/div/a[1]/img'
        try:
            WebDriverWait(browser, 3).until(ec.presence_of_element_located((By.XPATH, xp)))
            return True
        except:
            browser.quit()
            browser = SettingBrowser('./chromedriver.exe', True)
            return browser
    sleep(0.3)
    browser.find_element_by_xpath("//*[@id='cyberId']").clear()
    sleep(0.3)
    browser.find_element_by_xpath("//*[@id='cyberId']").send_keys(id)
    sleep(0.3)
    browser.find_element_by_xpath("//*[@id='cyberPass']").clear()
    sleep(0.3)
    browser.find_element_by_xpath("//*[@id='cyberPass']").send_keys(pw)
    sleep(0.3)
    browser.find_element_by_xpath("//*[@id='loginForm']/span/a/img").click()
    sleep(0.3)
    try:
        browser.find_element_by_xpath("//*[@id='loginForm']/span/a/img").click()
        sleep(0.3)
    except:
        pass
    xp = '//*[@id="mainBody"]/div/div[2]/div/fieldset/div/a[1]/img'
    try:
        WebDriverWait(browser, 5).until(ec.presence_of_element_located((By.XPATH, xp)))
        return True
    except:
        return False

def AcceptAlert(browser, worker_idx):
    try:
        WebDriverWait(browser, 3).until(ec.alert_is_present())
        alert = browser.switch_to.alert
        alert_txt = alert.text
        alert_txt = alert_txt.replace('\n', ' ')
        alert.accept()
    except Exception as e:
        return False

def FindResv(browser, resv, worker_idx):        # (area, date, time, order, phone_number)
    global today_month
    try:
        day = resv[1][0] + '.' + resv[1][1] + '.' + resv[1][2]

        if int(resv[1][1]) > today_month + 1:
            elem = WebDriverWait(browser, 5).until(ec.presence_of_element_located((By.XPATH, '//*[@id="container"]/div[3]/div[5]/div[2]/ul/li[1]/a')))
            elem.click()

        elem = WebDriverWait(browser, 5).until(ec.presence_of_element_located((By.XPATH, '//*[@day="' + day + '"]')))
        elem = elem.find_element_by_tag_name('a')
        title = elem.get_attribute('title')
        if title == '예약하기':
            elem.click()
            WebDriverWait(browser, 3).until(ec.presence_of_element_located((By.XPATH, '//*[@id="rsvTableBody"]/tr[1]')))
            elem = browser.find_element_by_xpath('//*[@id="rsvTableBody"]')
            t = resv[2] + '시 '
            elems = elem.find_elements_by_xpath("//*[contains(text(), '"+t+"')]")

            if len(elems) != 0:
                order = int(resv[3]) - 1
                if len(elems) <= order:
                    order = len(elems) - 1
                rsv_tr = elems[order].find_element_by_xpath("..")
                txt = rsv_tr.text
                next_order = order + 1
                if next_order == len(elems):
                    next_order = 0
                while ("셀프" in txt) and next_order != order:
                    rsv_tr = elems[next_order].find_element_by_xpath("..")
                    txt = rsv_tr.text
                    next_order += 1
                    if next_order == len(elems):
                        next_order = 0
                resv_button = rsv_tr.find_element_by_class_name('button')
                resv_button_js = resv_button.get_attribute("href")
                resv_button_js = resv_button_js[20:-2].split(',')
                resv_button_js = list(map(eval, resv_button_js))
                resv_button.click()
                AcceptAlert(browser, worker_idx)
                if resv[0] == "1" or resv[0] == "2":
                    # resv_button_js
                    # --> setFdata(fJiyukCd, fRsvD, fRsvT, fRsvDv, fGubunCd, fSelfYn, fRoundCode,
                    #               btClass, dcAmt, assn_ind_inwon, fGubunCode, fRoundInd, fAssnInd, fInTerms, fSelfCartYn)
                    if resv_button_js[11] == '2' or resv_button_js[11] == '27':
                        AcceptAlert(browser, worker_idx)
                    if resv_button_js[12] == '06' or resv_button_js[14] == '1':
                        # infoPop(1)
                        # /html/body/div[1]/div[3]/div/dl/dd[6]/a/img
                        elem = WebDriverWait(browser, 3).until(ec.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div/dl/dd[6]/a/img')))
                        elem.click()
                    if resv_button_js[12] == '09' or resv_button_js[13] == '01':
                        # infoPop(2)
                        # /html/body/div[1]/div[4]/div/dl/dd[6]/a/img
                        elem = WebDriverWait(browser, 3).until(ec.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[4]/div/dl/dd[6]/a/img')))
                        elem.click()
                elif resv[0] == "1":
                    # resv_button_js
                    # --> setFdata(fJiyukCd, fRsvD, fRsvT, fRsvDv, dcAmt, assn_ind, assn_ind_inwon, fRoundCode)
                    if resv_button_js[6] == '01':
                        AcceptAlert(browser, worker_idx)
                    elif resv_button_js[5] == '06':
                        elem = WebDriverWait(browser, 3).until(ec.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[5]/div/dl/dd[7]/a/img')))
                        elem.click()
                    elif resv_button_js[7] == '27':
                        AcceptAlert(browser, worker_idx)
                return True
            return False
    except Exception as e:
        return False

def MakeResv(browser, smsauth: SmsAuth, worker_idx: int):
    try:
        try:
            WebDriverWait(browser, 5).until(ec.presence_of_element_located((By.ID, 'answer')))
        except TimeoutException:
            return False
        if smsauth.has_phone_number():
            phone_number = smsauth.get_phone_number()
            browser.execute_script(f"$(\"#authPhoneNum1\").attr(\"value\", \"{phone_number[0]}\")")
            browser.execute_script(f"$(\"#authPhoneNum2\").attr(\"value\", \"{phone_number[1]}\")")
            browser.execute_script(f"$(\"#authPhoneNum3\").attr(\"value\", \"{phone_number[2]}\")")
        try:
            browser.execute_script("doSmsAuthSend()")
        except JavascriptException:
            return False
        WebDriverWait(browser, alert_waiting_t).until(ec.alert_is_present())
        browser.switch_to.alert.accept()
        answer = smsauth.OCR()
        try:
            browser.find_element_by_xpath("//*[starts-with(@id, 'answer')]").send_keys(answer)
        except ElementNotInteractableException:
            return False
        sleep(0.2)
        browser.execute_script("doSubmit()")
        try:
            browser.find_element_by_xpath('//*[@href="javascript:doExecute();"]').click()
        except:
            pass
        try:
            WebDriverWait(browser, alert_waiting_t).until(ec.alert_is_present())
        except TimeoutException:
            return False
        alert = browser.switch_to.alert
        alert_txt = alert.text
        alert_txt = alert_txt.replace('\n', ' ')
        alert.accept()
        if '[A01]' in str(alert_txt):
            return False
        return True
    except Exception as e:
        return False



