
import scrapy
import json

    
class MfcSpider(scrapy.Spider):
    name = "encyclopedia"

    def start_requests(self):
        cookies = {'TBv4_Hash': "e45c8a44504e74f182109d794424a1e8", 
                   'TBv4_Iden': "147481"
        }
        start_urls = [
        'https://myfigurecollection.net/entry/324529',
        ]
        
        yield scrapy.Request(url=start_urls[0], callback=self.parse, cookies=cookies)
 
    def parse(self, response):
        
        try:
            path = '/Users/kamiosu/Documents/PythonProjects/automfc/database/'
            #Returns a list of SelectorList objects, each containing a single card element which can be further parsed
            entry = response.css('.form .form-field')
            current_index = response.url.strip().split('/')[-1]
            data =  { 
                'id': current_index,
                'category': entry[0].css(".form-input a::text").get().lower(),
                'name': entry[1].css(".form-input strong::text").get(),
                'original_name': entry[2].css(".form-input::text").get()
                }
            print(data)     
            with open(path+f'{data["category"]}.json', 'a') as f: 
                f.write(',')
                json.dump(data, f, ensure_ascii=False)
                
        except Exception as e:
            print(e)
            pass
                    
        finally:
            next_page = f'https://myfigurecollection.net/entry/{int(current_index)+1}'
            if next_page is not None:
                cookies = {'TBv4_Hash': "e45c8a44504e74f182109d794424a1e8", 
                           'TBv4_Iden': "147481"
                }
                next_page=response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse, cookies=cookies)
                    
            