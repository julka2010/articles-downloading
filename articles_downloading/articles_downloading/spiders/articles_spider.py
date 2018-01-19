from urlparse import urlparse
import time

import scrapy

#TODO remove by xpath '//script[not(contains(@type, "text"))]'


class ArticlesSpider(scrapy.Spider):
    name = 'articles'

    def start_requests(self):
        start_urls = []

        # arguments
        urls_file = getattr(self, 'urls_file', None)
        if urls_file is not None:
            with open(urls_file) as urls:
                for url in urls:
                    start_urls.append(url)

        for url in start_urls:
            yield scrapy.Request(url, self.parse)

    def parse(self, response):
        for article in response.css('body'):
            parsed_url = urlparse(response.url)
            yield {
                'title': article.css('title').extract_first() or time.time(),
                'text': article.css('body').extract_first(),
                'source': response.url,
                'tags': ' '.join([
                    'article', '::'.join([
                        'blog', parsed_url.netloc, '::'.join(
                            parsed_url.path.split('/')[1:-1]
                        )
                    ])
                ]),
            }
#        follow links
#        for href in response.css('li.next a'):
#            yield response.follow(href, callback=self.parse)
