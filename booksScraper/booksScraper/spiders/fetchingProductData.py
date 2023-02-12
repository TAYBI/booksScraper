import scrapy
from scrapy.crawler import CrawlerProcess


class FetchingProductData(scrapy.Spider):
    name = 'books'
    start_urls = [
        'https://www.bookdepository.com/category/3391/Teen-Young-Adult']

    # global page_count
    # page_count = 1

    def parse(self, response):

        # paginationCount = int(len(response.css('.pagination a')) / 2 -1)

        books = response.css('.book-item')
        for book in books:
            yield {
                'title': book.css('.title a::text').get(),
                'author': book.css('.author span a span::text').get(),
                'published': book.css('.published::text').get(),
                'format': book.css('.format::text').get(),
                'price':  book.css('.price-wrap .price .sale-price::text').get().replace('US$', ''),
                'bookLink':  'https://www.bookdepository.com' + book.css('.title a').attrib['href']
            }

        # next_url = response.css('.top-category a::text').get()
        # response.css('.top-category a').attrib['href']``

        next_url = 'https://www.bookdepository.com' + \
            response.css('.next a').attrib['href']

        if next_url is not None:
            # yield scrapy.Request(url= next_url)
            yield response.follow(next_url, callback=self.parse)


c = CrawlerProcess({
    'USER_AGENT': 'Mozilla/5.0',
    'FEED_FORMAT': 'json',
    'FEED_URI': 'output.json',
})
c.crawl(FetchingProductData)
c.start()
