import scrapy

class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

 
    
    def parse(self, response):
        books=response.css('article.product_pod')
        for book in books:
            relative_url=book.css('h3 a').attrib['href']
            if 'catalogue/' in relative_url:
                book_url='https://books.toscrape.com/'+relative_url
            else:
                book_url='https://books.toscrape.com/catalogue/'+relative_url
            yield response.follow(book_url,callback=self.parse_book)

        next=response.css('li.next a ::attr(href)').get()
        if next is not None:
                if 'catalogue/' in next:
                     next_url='https://books.toscrape.com/'+next
                else:
                     next_url='https://books.toscrape.com/catalogue/'+next
                yield response.follow(next_url,callback=self.parse)
    def parse_book(self,response):
        rows=response.css('table tr')
        yield{
            "name":response.css('div.product_main h1::text').get(),
            'UPC':rows[0].css('td::text').get(),
            'Product_Type':rows[1].css('td::text').get(),
            'Price':response.css('p.price_color::text').get(),
            'Rating': response.css('p.star-rating').attrib['class']
        }
    