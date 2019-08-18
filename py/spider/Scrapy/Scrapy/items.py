import scrapy

class ScrapyItem(scrapy.Item):
    bookList = scrapy.Field()

class imageSrcItem(scrapy.Item):
    srcList = scrapy.Field()
