# -*- coding: utf-8 -*-
import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

import scrapy
from scrapy import Selector
from bs4 import BeautifulSoup
from finance_crawl.items import HistCrawlItem
from config import *
from const import *


class SinaSpider(scrapy.Spider):
    #import pdb;pdb.set_trace()
    name = "sina_crawl"
    allowed_domains = ['vip.stock.finance.sina.com.cn']

    def __init__(self, *args, **kwargs):
        super(SinaSpider, self).__init__(SinaSpider.name, **kwargs)
        self.start_year = kwargs.get('start_year', CONST_START_YEAR)
        self.end_year = kwargs.get('end_year', CONST_END_YEAR)
        self.stockid_str = kwargs.get('stockid_str', CONST_STOCK_ID_STR)

    def start_requests(self):
        '''
            url : http://vip.stock.finance.sina.com.cn/corp/go.php/vMS_MarketHistory/stockid/000016/type/S.phtml?year=2017&jidu=1
        '''
        # self.start_year = CONST_START_YEAR
        # self.end_year = CONST_END_YEAR
        # self.stockid_str = CONST_STOCK_ID_STR          

        for stockid in self.stockid_str.split(','):
            for year in xrange(int(self.start_year), int(self.end_year) + 1):
                for jidu in xrange(1,5):
                    url = 'http://vip.stock.finance.sina.com.cn/corp/go.php/vMS_MarketHistory/stockid/'+stockid+'/type/S.phtml?year='+str(year)+'&jidu='+str(jidu)
                    url_info_dict = {'stockid': stockid}
                    yield scrapy.Request(url=url, callback=self.parse, meta=url_info_dict)


    def parse(self, response):
        self.logger.info('Getting data from ' + response.url)
        # import pdb;pdb.set_trace()
        try:
            tr_data = BeautifulSoup(response.body, 'lxml').find('table', attrs={'id':'FundHoldSharesTable'}).find_all('tr')
            
            stockid = response.meta.get('stockid')
            for day_info in tr_data[2:]:
                td_data = day_info.find_all('td')
                price_day = td_data[0].find('div').a.string.strip('\r\n\t')
                open_price = td_data[1].find('div').get_text().strip('\r\n\t')
                highest_price = td_data[2].find('div').get_text().strip('\r\n\t')
                close_price = td_data[3].find('div').get_text().strip('\r\n\t')
                lowest_price = td_data[4].find('div').get_text().strip('\r\n\t')
                #close_price = td_data[3].xpath('div/text()').extract()[0]

                item_data = ','.join([stockid, price_day, open_price, highest_price, lowest_price, close_price])

                stock_crawl = HistCrawlItem()
                stock_crawl['data'] = item_data
                yield stock_crawl
            self.logger.info(response.url + ' data get done.')
        except:
            self.logger.error('unable to get data from ' + response.url)

        