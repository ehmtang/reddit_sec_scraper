from datetime import datetime
from configparser import ConfigParser
from scrapy.crawler import CrawlerProcess
from reddit_praw.wallstreetbets_praw import WallStreetBetsPraw
from scrapy_spiders.scrapy_spiders.spiders.spiders import WallStreetBetsSpider, Form8SECSpider
from utils.utils import Utils
from sec_edgar_access.sec_edgar_access import SecEdgarAccess


def main():
    # Read configuration file
    config = ConfigParser()
    config.read('config.cfg')

    # Today's date
    current_date = datetime.today().strftime('%Y-%m-%d')

    # Instantiate Reddit Praw API on subreddit forum WallStreetBets
    scraper = WallStreetBetsPraw(
        client_id=config.get('reddit_praw', 'client_id'),
        client_secret=config.get('reddit_praw', 'client_secret'),
        user_agent=config.get('reddit_praw', 'user_agent')
    )

    # Retreive headlines of top 100 daily posts and save as json file with today's date
    headlines = scraper.scrape_top_dailies_posts()
    Utils.export_to_json(data=headlines, file_name=f"wallstreetbets_headlines_{current_date}.json")

    # Retreive latest Form 4 from SEC EDGAR website belonging to Berkshire Hathaway
    headers = eval(config.get('edgar_search', 'headers'))
    sec_edgar_access = SecEdgarAccess(headers=headers)
    form4_url = sec_edgar_access.get_latest_form4_url(cik=config.get('edgar_search', 'cik'))[0]
    form4_date = sec_edgar_access.get_latest_form4_url(cik=config.get('edgar_search', 'cik'))[1]['reportDate'].iloc[0]

    # Initiate spiders and export txt file with today's date
    process = CrawlerProcess()
    process.crawl(WallStreetBetsSpider, file_name=f"active_tickers_{current_date}.txt")
    if form4_url:
        process.crawl(Form8SECSpider, url=form4_url, file_name=f"form4_{config.get('edgar_search', 'cik')}_{form4_date}.txt")
    process.start()
    process.stop()


if __name__ == '__main__':
    main()