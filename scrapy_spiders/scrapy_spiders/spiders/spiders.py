import scrapy
from utils.utils import Utils

class WallStreetBetsSpider(scrapy.Spider):
    name = "wallstreetbets_spider"
    start_urls = ['https://www.reddit.com/r/wallstreetbets/']
    
    def __init__(self, file_name=None, *args, **kwargs):
        super(WallStreetBetsSpider, self).__init__(*args, **kwargs)
        self.file_name = file_name

    def parse(self, response):
        rows = response.css("table tr")        
        table = [row.css("td::text").extract() for row in rows]
        Utils.export_to_txt(table, self.file_name)

class Form8SECSpider(scrapy.Spider):
    name = "form8_sec_spider"
    
    def __init__(self, file_name=None, url=None, *args, **kwargs):
        super(Form8SECSpider, self).__init__(*args, **kwargs)
        self.file_name = file_name
        self.url = url

    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse)
    
    def parse(self, response):
        rows = response.css("table:nth-of-type(3) tbody")
        table = [row.css("tr span.FormData::text").extract() for row in rows]
        Utils.export_to_txt(table, self.file_name)
