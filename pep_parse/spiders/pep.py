from urllib.parse import urljoin

import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        rows = response.css('table.pep-zero-table tr')
        for row in rows:
            cols = row.css('td')
            if not cols:
                continue
            number = cols[1].css('a::text').get()
            if number is None or number.strip() == '0':
                continue
            link = cols[1].css('a::attr(href)').get()
            if link is None:
                continue
            pep_url = urljoin(response.url, link)
            yield response.follow(
                pep_url,
                callback=self.parse_pep,
            )

    def parse_pep(self, response):
        item = PepParseItem()
        number = response.url.rstrip('/').split('-')[-1]
        item['number'] = str(int(number))
        title_parts = response.css('h1.page-title ::text').getall()
        title = ''.join(title_parts).strip()
        if '–' in title:
            title = title.split('–', 1)[1].strip()
        item['name'] = title
        status_dd = response.xpath(
            "//dt[contains(., 'Status')]/following-sibling::dd[1]"
        )
        status_text = ''
        if status_dd:
            abbr_text = status_dd.xpath('./abbr/text()').get()
            if abbr_text:
                status_text = abbr_text.strip()
            else:
                status_text = status_dd.xpath(
                    'string(.)'
                ).get('').strip()
        item['status'] = status_text
        yield item
