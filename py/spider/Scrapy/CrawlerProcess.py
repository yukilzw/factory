import scrapy
from scrapy.crawler import CrawlerProcess
from Scrapy.spiders.getSexyImg import DmozSpider
from scrapy.utils.project import get_project_settings

# 创建一个CrawlerProcess对象
process = CrawlerProcess(get_project_settings()) # 括号中可以添加参数

process.crawl(DmozSpider)
process.start()