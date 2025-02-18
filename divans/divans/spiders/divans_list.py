import scrapy


class DivansListSpider(scrapy.Spider):
    name = "divans_list"
    allowed_domains = ["divan.ru"]
    start_urls = ["https://www.divan.ru/category/divany-i-kresla"]

    def parse(self, response):
        for product in response.css('div._Ud0k'):
            item = {
                #'name':product.xpath('.//span[@itemprop="name"]/text()').get()
                'name': product.css('span[itemprop="name"]::text').get().strip(),
                #'price': product.css('span.price bdi::text').get().strip(),
                'price': product.css('meta[itemprop="price"]::attr(content)').get(),
                #'link': product.css('a::attr(href)').get()
                'url': response.urljoin(product.css('a::attr(href)').get())
            }
            #print(item)
            yield item
        next_page = response.css('a.pagination__next::attr(href)').get()
        if next_page=="https://www.divan.ru/category/divany-i-kresla/page-1":
            pass
        elif next_page:
                yield response.follow(next_page, self.parse)

