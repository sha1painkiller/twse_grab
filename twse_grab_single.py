# -*- coding: utf-8 -*-
import os
import re
import sys
import csv
import time
import string
import logging
import requests
import argparse
from lxml import html
from datetime import datetime, timedelta

class Crawler():
    def __init__(self, prefix="data"):
        ''' Make directory if not exist when initialize '''
        if not os.path.isdir(prefix):
            os.mkdir(prefix)
        self.prefix = prefix

    def _clean_row(self, row):
        ''' Clean comma and spaces '''
        for index, content in enumerate(row):
            row[index] = re.sub(",", "", content.strip())
        return row

    def get_data(self, stock, year, month):
        payload = {
            'download': '',
            'query_year': year,
            'query_month': month,
            'CO_ID': '2454'
        }
        url = 'http://www.twse.com.tw/ch/trading/exchange/STOCK_DAY/STOCK_DAYMAIN.php'

        # Get html page and parse as tree
        page = requests.post(url, data=payload)

        if not page.ok:
            logging.error("Can not get TSE data at {}".format(date_str))
            return

        # Parse page
        tree = html.fromstring(page.text)
        f = open('{}/{}.csv'.format(self.prefix, stock), 'a')
        cw = csv.writer(f, lineterminator='\n')

        for tr in tree.xpath('//table/tbody/tr'):
            tds = tr.xpath('td/text()')

            row = self._clean_row([
                tds[0],
                tds[1], # 成交股數
                tds[2], # 成交金額
                tds[3], # 開盤價
                tds[4], # 最高價
                tds[5], # 最低價
                tds[6], # 收盤價
                tds[7], # high/low gap
                tds[8], # 成交筆數
            ])
            cw.writerow(row)

        f.close()

if __name__ == '__main__':

    crawler = Crawler()
    crawler.get_data(2454, 2017, 2)

