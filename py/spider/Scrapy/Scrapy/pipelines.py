import os
import scrapy
import logging
import requests
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy.utils.project import get_project_settings

logger = logging.getLogger('myLog')

class ScrapyPipeline(object):
    def process_item(self, item, spider):
        item = dict(item)
        with open('img.txt', 'a+', encoding='utf-8') as f:
            titles = item['imgTitle']
            for title in titles:
                f.write(title + '\n')
        return item

class SaveImgPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        itemDic = dict(item)
        if 'bookList' not in itemDic:
            return
        bookList = itemDic['bookList']
        for book in bookList:
             yield scrapy.Request(url=book['logo'], meta={'name': book['name']})

    def item_completed(self, results, item, info):
        if not len(results):
            return item
        if not results[0][0]:
            raise DropItem('下载失败')
        logger.debug('下载图片成功')
        return item

    def file_path(self, request, response=None, info=None):
        name = request.meta['name'] + '.' + request.url.split('.')[-1]
        return name

class SaveDetailImgPipeline(ImagesPipeline):
    def process_item(self, item, spider):
        itemDic = dict(item)
        if 'srcList' not in itemDic:
            return item
        srcList = itemDic['srcList']
        setting = get_project_settings()
        for image in srcList:
            image_url = image['src']
            folder = setting.attributes['IMAGES_STORE'].value + '/' + image['name']
            if not os.path.exists(folder):
                os.makedirs(folder) 
            filePath = folder + '/' + image_url.split('/')[-1]
            with open(filePath, 'wb') as f:
                response = requests.get(image_url, stream=True)
                for block in response.iter_content(1024):
                    if not block:
                        break
                    f.write(block)
        return item