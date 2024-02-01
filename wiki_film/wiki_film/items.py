# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WikiFilmItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    en_name = scrapy.Field()
    producer = scrapy.Field()
    country = scrapy.Field()
    year = scrapy.Field()
    genres = scrapy.Field()
