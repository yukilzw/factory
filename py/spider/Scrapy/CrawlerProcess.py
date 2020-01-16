import scrapy
from scrapy.crawler import CrawlerProcess
from Scrapy.spiders.getSexyImg import DmozSpider
from scrapy.utils.project import get_project_settings

# creat CrawlerProcess project
process = CrawlerProcess(get_project_settings())

process.crawl(DmozSpider)
process.start()