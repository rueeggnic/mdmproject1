import scrapy

class GpxSpider(scrapy.Spider):
    name = "gpx"
    start_urls = [
        "http://www.hikr.org/filter.php?act=filter&a=ped&ai=100&aa=630"
    ]

    def parse(self, response):
        # Folge allen Links zu Wanderungen
        for href in response.css('.content-list a::attr(href)').getall():
            yield response.follow(href, self.parse_detail_page)

        # Weiter zur nächsten Seite
        next_page = response.css('a#NextLink::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_detail_page(self, response):
        gpx_href = [href for href in response.css('#geo_table a::attr(href)').getall() if href.endswith(".gpx")]

        if gpx_href:
            yield {
                "file_urls": [gpx_href[0]],
                "name": response.css('h1.title::text').get(),
                "difficulty": response.xpath(
                    'normalize-space(//td[normalize-space()="Hiking grading:"]/following-sibling::td/a/text())'
                ).get(),
                "user": response.css('.author a.standard::text').get(),
                "url": response.url,
            }
