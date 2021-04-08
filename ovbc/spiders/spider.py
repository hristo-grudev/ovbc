import re

import scrapy

from scrapy.loader import ItemLoader

from ..items import OvbcItem
from itemloaders.processors import TakeFirst


class OvbcSpider(scrapy.Spider):
	name = 'ovbc'
	start_urls = ['https://www.ovbc.com/community/news']

	def parse(self, response):
		post_links = response.xpath('//a[@data-link-type-id="page"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//div[@class="subpage-header"]//h1/text()').get()
		description = response.xpath('//div[@data-content-block="bodyCopy"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()
		date = re.findall(r'[A-Za-z]+\s\d{1,2},\s\d{4}', description) or ['']

		item = ItemLoader(item=OvbcItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date[0])

		return item.load_item()
