import scrapy
import json


class QuotesSpider(scrapy.Spider):
    name = "QuotesSpider"

    def start_requests(self):
        urls = [
            'http://quotes.toscrape.com/page/1/',
            'http://quotes.toscrape.com/page/2/',
        ]

        for url in urls:
            yield scrapy.Request(url, callback=self.parse)


    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f'quotes-{page}.json'

        quote_divs = response.css("div.quote")

        for cur_quote_div in quote_divs:
            text = cur_quote_div.css("span.text::text").get()
            author = cur_quote_div.css("small.author::text").get()
            tags = cur_quote_div.css("div.tags a.tag::text").getall()
            yield {
                "text": text,
                "author": author,
                "tags": tags
            }
