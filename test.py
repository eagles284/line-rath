import selenium.webdriver as webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as expected
from selenium.webdriver.support.wait import WebDriverWait

if __name__ == "__main__":
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    options.set_headless(headless=True)
    driver = Firefox(executable_path='/usr/local/bin/geckodriver', firefox_binary='/usr/bin/firefox' , firefox_options=options)
    driver.get('http://www.instagram.com')
    driver.quit()