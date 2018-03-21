# -*- coding: utf-8 -*-
import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

import scrapy
from scrapy import Selector
from bs4 import BeautifulSoup
from finance_crawl.items import HistCrawlItem
from config import *
from const import *

class NeteaseSpider(scrapy.Spider):
    name = "netease_crawl"
    allowed_domains = ['quotes.money.163.com']
    start_urls = []

    def start_requests(self):
        '''
            url : http://quotes.money.163.com/trade/lsjysj_zhishu_000016.html?year=2017&season=1
        '''
        self.start_year = CONST_START_YEAR
        self.end_year = CONST_END_YEAR
        self.stockid_str = CONST_STOCK_ID_STR    
  
        for stockid in self.stockid_str.split(','):
            for year in xrange(self.start_year, self.end_year + 1):
                for jidu in xrange(1,5):
                    url = 'http://quotes.money.163.com/trade/lsjysj_zhishu_'+stockid+'.html?year='+str(year)+'&season='+str(jidu)
                    url_info_dict = {'stockid': stockid}
                    yield scrapy.Request(url=url, callback=self.parse, meta=url_info_dict)
    

    def parse(self, response):
        #import pdb;pdb.set_trace()
        self.logger.info('Getting data from ' + response.url)
        try:
            tr_data = BeautifulSoup(response.body, 'lxml').find('table', attrs={'class':'table_bg001 border_box limit_sale'}).find_all('tr')
            
            stockid = response.meta.get('stockid')
            for day_info in tr_data[1:]:
                td_data = day_info.find_all('td')
                price_day = td_data[0].get_text().strip('\r\n\t').replace(',', '')
                price_day = price_day[0:4] + '-' + price_day[4:6] + '-' + price_day[6:8]
                open_price = td_data[1].get_text().strip('\r\n\t').replace(',', '')
                highest_price = td_data[2].get_text().strip('\r\n\t').replace(',', '')
                lowest_price = td_data[3].get_text().strip('\r\n\t').replace(',', '')
                close_price = td_data[4].get_text().strip('\r\n\t').replace(',', '')
                #close_price = td_data[3].xpath('div/text()').extract()[0]

                item_data = ','.join([stockid, price_day, open_price, highest_price, lowest_price, close_price])

                stock_crawl = HistCrawlItem()
                stock_crawl['data'] = item_data
                yield stock_crawl
            self.logger.info(response.url + ' data get done.')
        except:
            self.logger.error('unable to get data from ' + response.url)

        