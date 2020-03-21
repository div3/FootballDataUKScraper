import scrapy

class ResultData(scrapy.Spider):
	name="ResultData"

	def start_requests(self):
		origin = "http://www.football-data.co.uk/data.php"
		yield scrapy.Request(url=origin, callback=self.init_parse)

	def init_parse(self, response):
		links = response.xpath("//table[5]//tr[2]/td[3]/table/tr/td/a/@href").getall()
		for link in links:
			yield response.follow(link, callback=self.parse)

	def parse(self, response):
		data_list = response.xpath('//table[5]//tr[2]/td[3]/a/@href').getall()
		for data in data_list:
			yield response.follow(data, callback=self.save)

	def save(self, response):
		url = response.url.split("/")
		begin = "/Users/divyansh/Documents/Projects/Soccer/scraped_data/"
		filename = begin + url[4] + "_" + url[5]
		with open(filename, 'wb') as f:
			f.write(response.body)
			f.close()
			print(filename, ' saved')
