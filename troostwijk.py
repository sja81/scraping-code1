from tokenize import String
from selenium.webdriver.common.by import By
from auction import AuctionGroup

class Troostwijk:
    groups = []

    def __init__(self) -> None:
        self.base_url = "https://www.troostwijkauctions.com/uk/auction-calendar"
        self.base_tag = "sale"

    def get_base_url(self) -> str:
        return self.base_url    

    def get_base_tag(self) -> str:
        return self.base_tag

    def process_group(self, elements) -> None:
        try:
            for _ix in elements:
                group = AuctionGroup()

                group.set_url(self.__process_url(_ix))
                group.set_title(self.__process_title(_ix))
                group.set_town(self.__process_town(_ix))
                group.set_country(self.__process_country(_ix))

                self.groups.append(group)
                del group
        except Exception as e:
            print(e)
        return        

    def __process_url(self, elem) -> str:
        _url = elem.find_element(By.XPATH, ".//div[@class='details']/a")
        return _url.get_attribute("href")

    def __process_title(self, elem) -> str:
        _title = elem.find_element(By.XPATH, './/h2')
        return _title.text

    def __process_town(self, elem) -> str:
        _town = elem.find_element(By.XPATH, ".//div[@class='details']/div[@class='location-lots']/div[@class='location']/div/span[@class='city']")
        return _town.text

    def __process_country(self, elem) -> str:
        _country = elem.find_element(By.XPATH, ".//div[@class='details']/div[@class='location-lots']/div[@class='location']/div/span[@class='country']")
        return _country.get_attribute("content")

