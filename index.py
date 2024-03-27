from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from item.filter_information import getInfo, info
from item.terminal import Effect, Table, Account
from datetime import datetime
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from item.tool import game_pass, buyer
import time, os, json
table = Table()
def CheckItem(driver, id,time):
    try:
        WebDriverWait(driver, time).until(  # Timeout sau 5 giây
            EC.visibility_of_element_located((By.ID, id))
        )
        return True
    except TimeoutException:
        return False


def CheckInfoLogin(driver, name, username, pack, money, timeN):
    failLogin = CheckItem(driver, "login-form-error", 1)
    if failLogin == True:
        table.add_row(id, name, username, pack, money, timeN, "❌ Sai tk/mk")
        return
    twoStep = CheckItem(driver, "two-step-verification-code-input", 1)
    if twoStep == True:
        table.add_row(id, name, username, pack, money, timeN, "❌ 2 step")
        return
    

current_working_directory = os.getcwd()
capsolver_extension_path = current_working_directory + r"\CapSolver.Browser.Extension-chrome-v1.11.0"

chrome_options = webdriver.ChromeOptions()


chrome_options.add_argument(
    "--load-extension={0}".format(capsolver_extension_path), 
)


def login(id, name, username, password, pack, money, timeN, robux):

    with open("..\input.txt", "r", encoding="utf-8") as file:
        lines = [line.strip() for line in file.readlines()]
        buyerCookie = lines[0].split("/")[2]

    if robux == 0:
        return

    # Khởi tạo trình duyệt
    driver = webdriver.Chrome(options=chrome_options, service=ChromeService(ChromeDriverManager().install()))

    # Truy cập trang web
    driver.get("https://www.roblox.com/login")



    # Điền tài khoản và mật khẩu
    if driver.find_element(By.ID, "login-username").size['width'] != 0:
        driver.find_element(By.ID, "login-username").send_keys(username)

    if driver.find_element(By.ID, "login-password").size['width'] != 0:
        driver.find_element(By.ID, "login-password").send_keys(password)

    # Nhấp nút đăng nhập
    login_button = driver.find_element(By.ID, "login-button")
    login_button.click()

    # Chờ 2-3 giây để captcha tải (tùy chỉnh thời gian)

    try:
        WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'challenge-captcha-close-button')))
        try:

            WebDriverWait(driver, 60).until(EC.url_to_be("https://www.roblox.com/home"))
            cookies = driver.get_cookies()
            for cookie in cookies:
                if cookie['name'] == ".ROBLOSECURITY":
                    value = cookie["value"]
                    IDUNIVERSE = info.getUniverseId(value)
                    idGamepass = game_pass(value).pass_creator(robux,IDUNIVERSE)
                    buyer(buyerCookie).buy(False, idGamepass, "gamepass")  
                    table.add_row(id, name, username, pack, money, timeN, "✅")
                    break
        except TimeoutException:
            CheckInfoLogin(driver, name, username, pack, money, timeN)
            cookies = driver.get_cookies()
            for cookie in cookies:
                if cookie['name'] == ".ROBLOSECURITY":
                    value = cookie["value"]
                    IDUNIVERSE = info.getUniverseId(value)
                    idGamepass = game_pass(value).pass_creator(robux,IDUNIVERSE)
                    buyer(buyerCookie).buy(False, idGamepass, "gamepass")                    
                    table.add_row(id, name, username, pack, money, timeN, "✅")


                    break
    except TimeoutException:
            CheckInfoLogin(driver, name, username, pack, money, timeN)
            cookies = driver.get_cookies()
            for cookie in cookies:
                if cookie['name'] == ".ROBLOSECURITY":
                    value = cookie["value"]
                    IDUNIVERSE = info.getUniverseId(value)
                    idGamepass = game_pass(value).pass_creator(robux,IDUNIVERSE)
                    buyer(buyerCookie).buy(False, idGamepass, "gamepass")
                    table.add_row(id, name, username, pack, money, timeN, "✅")
                    break
    finally: 
        table.show_table()
        driver.quit()

    # Đóng trình duyệt
    
