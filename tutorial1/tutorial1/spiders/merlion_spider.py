from pathlib import Path

import scrapy


class MerlionSpider(scrapy.Spider):
    name = "merlion"

    def start_requests(self):
        urls = [
            "https://en.wikipedia.org/wiki/Singapore",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        hxs = scrapy.Selector(response)
        location = "Merlion"
        # extract all links from page
        all_links = hxs.xpath("*//a/@href").extract()

        for link in all_links:
            if location in link:
                yield scrapy.http.Request(
                    url="https://en.wikipedia.org" + link, callback=self.parse_merlion
                )

    def parse_merlion(self, response):
        filename = f"merlion_info.html"
        Path(filename).write_bytes(response.body)
        self.log(f"Saved file {filename}")
        # url = response.xpath('//div[@class="mw-parser-output"]/p/a')
        # for a in url:
        #     link = a.xpath("href").extract()
        #     yield link
        # page = response.url.split("/")[-2]
        # filename = f"quotes-{page}.html"
        # Path(filename).write_bytes(response.body)
        # self.log(f"Saved file {filename}")
        # title = response.css("a::text").extract
        # # for i in title:
        # #     if "Merlion" in i:
        # yield {"title": title}
        # filename = f"merlion_info.html"
        # Path(filename).write_bytes(response.body)
        # self.log(f"Saved file {filename}")
