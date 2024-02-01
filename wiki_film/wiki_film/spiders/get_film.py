import scrapy
import requests
import time
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

from wiki_film.items import WikiFilmItem


class GetFilmSpider(scrapy.Spider):
    name = "get_film"
    allowed_domains = ["ru.wikipedia.org", "imdb.com"]
    start_urls = ["https://ru.wikipedia.org/wiki/Категория:Фильмы_по_годам"]

        


    def parse(self, response):
        films = response.xpath('//div[@id="mw-pages"]//div[@class="mw-content-ltr"]//ul//li//a')
        yield from response.follow_all(films, self.parse_film)

        next_page = response.xpath("//a[contains(., 'Следующая страница')]")
        if next_page:
            yield from response.follow_all(next_page, self.parse)   

        pagination_films_links = response.xpath("//a[starts-with(@title,'Категория:Фильмы') and contains(@title,' года')]")
        yield from response.follow_all(pagination_films_links, self.parse)


    
    def parse_film(self, response):

        name =  response.xpath('//table[starts-with(@class, "infobox infobox")]//th[@class="infobox-above"]/text()').get()
        if not name:
            name = response.xpath("//div[@class='mw-content-ltr mw-parser-output']//b//text()").get()
            
        genres = response.xpath("//span[@data-wikidata-property-id='P136']//text()").getall() 
        year = response.xpath("//a[contains(@title, ' год')]/text()").re('(\d{4})')[0]
        country = response.xpath("//span[@data-wikidata-property-id='P495']//span[@class='wrap']//text()").get()
        if country is None:
            country = response.xpath("//span[@class='country-name']//text()").get()
        producer =  response.xpath("//span[@data-wikidata-property-id='P57']//text()").get()

        imdb_link = response.xpath("//span[@data-wikidata-property-id='P345']//a//@href").get()

        data_dict = {
                    "name" : name,
                    "genres" : genres,
                    "year" : year,
                    "country" : country,
                    "producer" : producer,
                    "imdb_rating": "",
                    "link" :   response.url
                }

        if imdb_link:
            yield scrapy.Request(imdb_link, callback=self.parse_imdb,
                                  headers={'User-Agent': UserAgent().chrome},
                                  cb_kwargs={"data":data_dict})
        else:
            yield  data_dict

            
    def parse_imdb(self, response, data):
        # rating = requests.get(response.url, headers={'User-Agent': UserAgent().chrome}).content
        # first = rating.find(b'<span class="sc-bde20123-1 cMEQkK">') + 35
        # second = rating.find(b'</span', first)
        # if second - first > 5:
        #     rating = "-"
        # else:
        #     rating = rating[first:second].decode()
        data['imdb_rating'] = response.xpath("//span[@class='sc-bde20123-1 cMEQkK']//text()").get()
        yield data



        


