# Imports
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import pandas as pd

# Constants
WEB = 'https://eltiempo.es'
DRIVER_PATH = 'C:\\chromedriver.exe'
CITY = 'Sevilla'
CSV_FILE = 'src/output/weather_today.csv'


def main():
    # Navigation options
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument('--start-maximized')
    options.add_argument('--disable-extensions')

    # Driver
    driver_path = DRIVER_PATH
    driver = webdriver.Chrome(executable_path=driver_path, options=options)
    # Driver init
    driver.get(WEB)

    # References
    id_cookies = 'didomi-notice-agree-button'
    id_input = 'inputSearch'
    class_search = 'button.form_search_submit'
    class_city = 'i.icon_weather_s icon icon-local'.replace(' ', '.')
    xpath_2tab = '/html/body/div[7]/main/div[4]/div/section[4]/section/div/article/section/ul/li[2]/a'
    xpath_today = '/html/body/div[7]/main/div[4]/div/section[4]/section/div[1]/ul/li[1]/ul'

    # Commands
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, id_cookies))).click()
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, id_input))).send_keys(CITY)
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, class_search))).click()
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, class_city))).click()
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, xpath_2tab))).click()

    # References today
    today_ul = driver.find_element_by_xpath('/html/body/div[7]/main/div[4]/div/section[4]/section/div[1]/ul/li[1]/ul')
    # Count today hours (it depends on the moment in which you consult)
    today_li_list = today_ul.find_elements_by_tag_name("li")

    # Lists
    hours = list()
    temps = list()
    wind_speeds = list()

    # Auxiliary string to not repeat in the 'for'
    col = '/html/body/div[7]/main/div[4]/div/section[4]/section/div[1]/ul/li[1]/ul'

    for i in range(1, len(today_li_list)+1):
        hours.append(driver.find_element_by_xpath(f'{col}/li[{i}]/span').text)
        temps.append(driver.find_element_by_xpath(f'{col}/li[{i}]/dl/dd[2]').text)
        wind_speeds.append(driver.find_element_by_xpath(f'{col}/li[{i}]/dl/dd[4]/span[2]').text)

    # Dataframe export to CSV
    df = pd.DataFrame({'Horas ': hours, 'Temperatura ': temps, 'Viento (Km/h) ': wind_speeds})
    print(df)
    df.to_csv(CSV_FILE, index=False)

    # Quit
    driver.quit()


if __name__ == "__main__":
    main()
