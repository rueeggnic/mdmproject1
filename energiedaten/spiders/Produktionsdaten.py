import scrapy


class ProduktionsdatenSpider(scrapy.Spider):
    name = "Produktionsdaten"
    allowed_domains = ["www.energiedashboard.admin.ch"]
    start_urls = ["https://www.energiedashboard.admin.ch/dashboard"]

    def parse(self, response):
        pass
