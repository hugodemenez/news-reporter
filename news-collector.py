import requests
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

class WebAgent:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super(WebAgent, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self._headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/95.0.4638.69 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
        }

    def __call__(self, *args, **kwargs):
        return self.get(*args, **kwargs)

    def get(self, url: str, params: dict = {}):
        response = requests.get(url, headers=self._headers, params=params)
        response.raise_for_status()
        return response
    
    def get_stocktwits_news(self, symbol:str = "BTC") -> str:

        """Get 10 latest news from stocktwits website about a crypto symbol"""
        logger.warning('Getting news from stocktwits')

        url = f"https://stocktwits.com/symbol/{symbol}.X/news"
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
        }

        response = requests.get(url, headers=headers)
        logger.warning(f"Response status code: {response.status_code}")
        soup = BeautifulSoup(response.content,features="html.parser")
        news_elements = soup.find_all("div",class_='NewsItem_textContainer__6FGsX')
        content = str()
        for index,news in enumerate(news_elements):
            title = news.find("span", class_="")
            date = news.find("span",class_="text-light-grey")
            content+=f"{index+1}. {title.text} - {date.text.split('•')[1]}\n"
        return content


    def get_coinmarketcap_news(self, symbol:str = "BTC") :
        """Get latest news from coinmarketcap website about a crypto symbol"""
        response = self.get("https://coinmarketcap.com/headlines/news/")
        content = response.content
        soup = BeautifulSoup(response.content,features="html.parser")
        news_elements = soup.find_all("a")
        news_summary = soup.find_all("p")
        content = str()
        for index,news in enumerate(news_elements):
            title = news
            if title and len(title.text) > 30:
                content+=f"{index+1}. {title.text}\n"
        for index,summary in enumerate(news_summary):
            if summary and len(summary.text) > 30:
                content+=f"{index+1}. {summary.text}\n"
        print(content)
        with(open("coinmarketcap_news.txt","w")) as f:
            f.write(content)
        return 


if __name__ == "__main__":
    print(WebAgent().get_coinmarketcap_news())
