# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
from config import *
from const import *

class FinanceCrawlPipeline(object):
    def process_item(self, item, spider):
    	return item



class SaveToFilePipeline(object):
	def __init__(self):
		self.file = None
		
	def open_spider(self, spider):
		self.data_file = DATA_PATH + spider.name.split('_')[0] + '_data'
		if os.path.exists(self.data_file):
			os.system("rm -f" + self.data_file);
		self.file = open(self.data_file, 'w')

	def process_item(self, item, spider):
		self.file.write(item['data'] + '\n')

	def close_spider(self, spider):
		self.file.close()
		self.post_process_data_sh()

	def post_process_data_sh(self):
		os.system("sh split_file.sh " + self.data_file.split('/')[-1] + " " + CONST_STOCK_ID_STR)
		# os.system("sh split_file.sh " + self.data_file + CONST_STOCK_ID_STR)
