class Auction(object):
    def __init__(self) -> None:
        self.__town = None
        self.__title = None
        self.__url = None
        self.__country = None

    def set_title(self, title: str) -> None:
        self.__title = title

    def get_title(self) -> str:
        return self.__title

    def set_url(self, url: str) -> None:
        self.__url = url

    def get_url(self) -> str:
        return self.__url
    
    def set_town(self, town: str) -> None:
        self.__town = town

    def get_town(self) -> str:
        return self.__town

    def set_country(self, country: str) -> None:
        self.__country = country

    def get_country(self) -> str:
        return self.__country


class AuctionGroup(Auction):
    def __init__(self):
        self.__lots = None
        self.__status = None
        self.__start_date = None

    def set_lots(self, lots: int) -> None:
        self.__lots = lots

    def get_lots(self) -> int:
        return self.__lots

    def get_start_date(self) -> str:
        return self.__start_date

    def set_start_date(self, start_date: str) -> None:
        self.__start_date = start_date

    def get_status(self) -> str:
        return self.__status

    def set_status(self, status: str) -> None:
        self.__status = status

    

class AuctionItem(Auction):
    
    def __init__(self) -> None:
        self.__group_id = None
        self.__last_bid = None
        self.__description = None




    