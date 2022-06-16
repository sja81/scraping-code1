"""This module will scrape the data from the auction page"""

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import mysql.connector
from troostwijk import Troostwijk


def write_group(conx, title: str, url: str, town: str, country: str, lots: int, status: str, start_date: str) -> None:
    add_group = ("INSERT INTO `groups` (`title`,`url`,`town`,`country`,`lots`,`status`,`start_date`) "
                "VALUES (%(title)s,%(url)s,%(town)s,%(country)s,%(lots)s,%(status)s,%(start_date)s)"
                )

    conx.execute(add_group,
                    {
                        'title': title,
                        'url': url,
                        'town': town,
                        'country': country,
                        'lots': lots,
                        'status': status,
                        'start_date': start_date
                    }
                )
    return

to_scrape = Troostwijk()

driver = webdriver.Chrome()
driver.get(to_scrape.get_base_url())

wait = WebDriverWait(driver, 30, poll_frequency=0.1)
wait.until(EC.visibility_of_element_located((By.CLASS_NAME, to_scrape.get_base_tag())))
    
elements = driver.find_elements(By.CLASS_NAME, to_scrape.get_base_tag())

cnx = mysql.connector.connect(host="localhost", user="root", password="", database="auction")
cursor = cnx.cursor()

try:
    
    for _ix in elements:
        _title = _ix.find_element(By.XPATH, './/h2')
        _url = _ix.find_element(By.XPATH, ".//div[@class='details']/a")
        _town = _ix.find_element(By.XPATH, ".//div[@class='details']/div[@class='location-lots']/div[@class='location']/div/span[@class='city']")
        _country = _ix.find_element(By.XPATH, ".//div[@class='details']/div[@class='location-lots']/div[@class='location']/div/span[@class='country']")
        try:
            _lots = _ix.find_element(By.XPATH,".//div[@class='details']/div[@class='location-lots']/span[@class='number-of-lots']")
            lots = int(_lots.text.replace('lot','').replace('s','').strip())
        except NoSuchElementException:
            lots = 0

        try:
            _status = _ix.find_element(By.XPATH,".//div[@class='details']/div[@class='date-countdown']/div/div")
            status = "active"
            if _status.get_attribute('class').strip().find("countdown closed") != -1:
                status = "closed"           
        except NoSuchElementException:
            status = "pending"

        # refactor to method with recursive call!!!!
        try:
            _start_date = _ix.find_element(By.XPATH,".//div[@class='details']/div[@class='date-countdown']/div/div/span[@class='date-label close-date']/span[@itemprop='startDate']")
        except NoSuchElementException:    
            _start_date = _ix.find_element(By.XPATH,".//div[@class='details']/div[@class='date-countdown']/span[@class='date-label close-date']/span[@itemprop='startDate']")

        write_group( cursor , 
            _title.text, 
            _url.get_attribute('href'), 
            _town.text, 
            _country.get_attribute("content"), 
            lots,
            status,
            _start_date.get_attribute("content")
        )
        cnx.commit()
except Exception as e:
    print(e)
    cnx.rollback()

cursor.execute()



cursor.close()
cnx.close()
driver.close()