import re
import scrapy


class ProxiesSpider(scrapy.Spider):
    name = 'proxies_spider'
    allowed_domains = ['http://www.nntime.com/proxy-list-01.htm']
    start_urls = ['http://www.nntime.com/proxy-list-01.htm']

    def parse(self, response, **kwargs):
        pattern = r'\(([^\[\]]+)\)'
        script_text = response.xpath('//head//script/text()').get()
        lst = script_text.strip().split(';')
        dct = {}
        for i in lst:
            if i != '':
                ind = i.index('=')
                key = i[:ind]
                value = i[ind + 1:]
                dct[key] = value

        for row in response.xpath('//*[@class="data"]//tr')[2:]:
            port_expression = row.css('td script::text').get()
            keys_str = str(re.findall(pattern, port_expression)[0])
            keys_list = keys_str.split('+')[1:]
            port = ''
            for i in keys_list:
                port += str(dct[i])

            yield {
                'ip': row.css('td::text').getall()[0],
                'port': port,
            }
