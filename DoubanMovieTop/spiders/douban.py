import scrapy
from DoubanMovieTop.items import DoubanmovietopItem

class DoubanSpider(scrapy.Spider):
    name = 'douban'
    #allowed_domains = ['movie.douban.com']
    def start_requests(self):
        start_urls = 'https://movie.douban.com/top250'
        yield scrapy.Request(start_urls)

    def parse(self, response):
        item = DoubanmovietopItem()
        movies = response.xpath('//ol[@class="grid_view"]/li')
        for movie in movies:
            item['ranking'] = movie.xpath('.//div[@class="pic"]/em/text()').extract()[0]
            item['movie_name'] = movie.xpath('.//div[@class="hd"]/a/span[1]/text()').extract()[0]
            item['score'] = movie.xpath('.//div[@class="star"]/span[@class="rating_num"]/text()').extract()[0]
            item['score_num'] = movie.xpath('.//div[@class="star"]/span/text()').re(r'(\d+)人评价')[0]  #Selector也有一种.re()
            yield item
        next_url = response.xpath('//span[@class="next"]/a/@href').extract()
        if next_url:
            next_url = 'https://movie.douban.com/top250' + next_url[0]
            yield scrapy.Request(next_url)