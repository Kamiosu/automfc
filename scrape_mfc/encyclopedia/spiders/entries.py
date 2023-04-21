
import scrapy
from pathlib import Path

class MfcSpider(scrapy.Spider):
    name = "encyclopedia"
    start_urls = [
        'https://myfigurecollection.net/entries.php?mode=browse&current=keywords&entryId=0&categoryId=3&noDescription=0&noOriginalName=0&isOrphan=0&isDraft=0&sort=date&order=desc&clubId=0&page=1',
    ]

 
    def parse(self, response):
        #Returns a list of SelectorList objects, each containing a single card element which can be further parsed
        for entry in response.css('.result'):
            yield { 
                'id': entry.css("div .tbx-tooltip::attr(href)").get().strip().split('/')[-1],
                'category': entry.css("div .stamp-category::text").get(),
                'name': entry.css("div .tbx-tooltip::text").get(),
                'original_name': entry.css("div .stamp-meta::text").get()
                }
            
            next_page = response.css('.nav-next::attr(href)').get()
            if next_page is not None:
                next_page=response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse)
                
            