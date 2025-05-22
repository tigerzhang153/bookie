import scrapy
class tableSpider(scrapy.Spider):
    name= 'table'
    
    start_url =[
        "https://sportsdatabase.com/nba/query?output=default&sdql=date%2C+team%2C+site%2C+o%3Ateam%2C+total%2C++points%2C+o%3Apoints+%40season%3E2010&submit=++S+D+Q+L+%21++"
    ]

    def parse(self, response):
        for row in response.xpath('//*[@class="dataTables_wrapper no-footer"]//tbody/tr'):
            if row.xpath('td[3]//text()').extract_first() == "home":
                yield {
                    'date' : row.xpath('td[1]//text()').extract_first(),
                    'team' : row.xpath('td[2]//text()').extract_first(),
                    'site' : row.xpath('td[3]//text()').extract_first(),
                    'o:team' : row.xpath('td[4]//text()').extract_first(),
                    'total' : row.xpath('td[5]//text()').extract_first(),
                    'points' : row.xpath('td[6]//text()').extract_first(),
                    'o:points' : row.xpath('td[7]//text()').extract_first(),
                } 