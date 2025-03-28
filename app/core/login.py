from selenium.webdriver.common.by import By
from app.config import USERNAME, PASSWORD
import time

LOGIN_URL = "https://ipssalta.gob.ar/SeguroEscolar/login.aspx"

def login(driver):
    driver.get(LOGIN_URL)
    time.sleep(2)
    print ("Username: ", USERNAME)
    print ("Password: ", PASSWORD)
    driver.find_element(By.ID, "txtUserName").send_keys(USERNAME)
    driver.find_element(By.ID, "txtPassword").send_keys(PASSWORD)
    driver.find_element(By.ID, "btnLogin").click()
    time.sleep(3)
    print("[✔] Login exitoso.")

    print("[*] Cookies de sesión activas:")
    for cookie in driver.get_cookies():
        print(f"   {cookie['name']} = {cookie['value']}")
