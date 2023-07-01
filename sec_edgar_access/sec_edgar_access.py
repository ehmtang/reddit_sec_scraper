import pandas as pd
import requests
import os.path
from utils.utils import Utils
from configparser import ConfigParser

config = ConfigParser()
config.read('config.cfg')
export_directory = config.get('utils', 'export_directory')

class SecEdgarAccess:
    LAST_KNOWN_RECORD_FILE = 'last_known_filing_date_record.csv'
    
    def __init__(self, headers):
        self.headers = headers
    
    def get_latest_form4_url(self, cik):
        filings_json = self._get_filings_json(cik)
        form4_filings = self._filter_form4_filings(filings_json)
        latest_filing_date_record = self._get_latest_filing_record(form4_filings)
        return self._get_form4_url(cik, latest_filing_date_record), latest_filing_date_record
    
    def _get_filings_json(self, cik):
        response = requests.get(f'https://data.sec.gov/submissions/CIK{cik}.json', headers=self.headers)
        response_json = response.json()
        return response_json['filings']['recent']
    
    def _filter_form4_filings(self, filings_json):
        filings_df = pd.DataFrame.from_dict(filings_json)
        filings_df['filingDate'] = pd.to_datetime(filings_df['filingDate'])
        return filings_df[filings_df['form'] == '4']
    
    def _get_latest_filing_record(self, form4_filings):
        last_known_record_file = os.path.join(export_directory, self.LAST_KNOWN_RECORD_FILE)
        last_known_record = pd.read_csv(last_known_record_file) if os.path.isfile(self.LAST_KNOWN_RECORD_FILE) else None
        latest_record = form4_filings.sort_values('filingDate').tail(1)
        if last_known_record is None or latest_record['filingDate'].iloc[0] > pd.to_datetime(last_known_record['filingDate'].iloc[0]):
            Utils.export_to_csv(latest_record, self.LAST_KNOWN_RECORD_FILE)
            return latest_record
        else:
            return None
    
    def _get_form4_url(self, cik, filing_record):
        if filing_record is None:
            return None
        accession_number = filing_record['accessionNumber'].str.replace('-', '').iloc[0]
        primary_document = filing_record['primaryDocument'].iloc[0]
        return f"https://www.sec.gov/Archives/edgar/data/{cik}/{accession_number}/{primary_document}"
