import scrapy
from Scrapy.items import ScrapyItem,imageSrcItem

class DmozSpider(scrapy.Spider):
    name = 'getSexyImg'
    page = 0
    pageEnd = 1
    host = 'http://www.tu11.com'
    def start_requests(self):
        yield scrapy.Request(url=self.host+'/meituisiwatupian/list_2_1.html', callback=self.parse)

    def parse(self, response):
        self.page += 1
        item = ScrapyItem() 
        bookList = []
        boxList = response.xpath('//div[@class="container pic4list"]//li[@class="col-xs-1-5"]/div')
        for box in boxList:
            inf = {
                'logo': box.xpath('.//img/@src').extract()[0],
                'name': box.xpath('.//img/@alt').extract()[0],
                'url': box.xpath('./a/@href').extract()[0],
                'time': box.xpath('.//span[@class="time"]/text()').extract()[0]
            }
            bookList.append(inf)
            yield scrapy.Request(url=self.host + inf['url'], callback=self.parseNewPage, meta=inf)
        item['bookList'] = bookList
        yield item


        nextBtn = response.xpath('//div[@class="pageinfo"]/li[last()-1]')
        btnClassName = nextBtn.xpath('./@class').extract()
        if not (len(btnClassName) and btnClassName != 'thisclass') and self.page < self.pageEnd:
            yield scrapy.Request(url=nextBtn.xpath('./a/@href').extract()[0], callback=self.parse)

    
    def parseNewPage(self, response):
        item = imageSrcItem()
        srcList = []
        imgList = response.xpath('//div[@class="nry"]//img/@src')
        for src in imgList:
            inf = {
                'name': response.meta['name'],
                'src': src.extract()
            }
            srcList.append(inf)
        item['srcList'] = srcList
        yield item

        nextBtnList = response.xpath('//div[@class="row dede_pages"]//li/a')
        for nextBtn in nextBtnList:
            btnText = nextBtn.xpath('./text()').extract()[0]
            if btnText == '下一页':
                cut = '/'
                urlCut = response.url.split(cut)
                urlCut[-1] = nextBtn.xpath('./@href').extract()[0]
                newUrl = cut.join(urlCut)
                yield scrapy.Request(url=newUrl, callback=self.parseNewPage, meta=response.meta)
