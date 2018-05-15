# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

class TutorialPipeline(object):

    def open_spider(self, spider):
        self.file = open('data.csv', 'a')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        # print('asd:', item)
        # self.file.write(json.dumps(dict(item), ensure_ascii=False))

        data = dict(item)
        line = '\t'.join([data['name'], data['type'], data['employers_count'], data['industry'], data['address'], data['website'], data['introduction']])
        self.file.write(line + '\n')

        return item
