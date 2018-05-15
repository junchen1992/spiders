import re

import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    custom_settings = {
        'DEPTH_LIMIT': 0,
        # 'REQUEST_DEPTH_MAX': 10
    }

    company_types = ['外资(欧美)', '外资(非欧美)', '合资', '国企', '民营公司', '外企代表处', '政府机关',
                     '事业单位', '非营利组织', '上市公司', '创业公司']

    def start_requests(self):
        urls = [
            # dalian
            'https://search.51job.com/list/230300,000000,0000,00,9,99,%2520,1,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=',
            # qingdao
            # 'https://search.51job.com/list/120300,000000,0000,00,9,99,%2520,1,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        jobs = response.css('div.dw_table div.el span.t2')
        com_urls = jobs.css('a::attr(href)').extract()
        for com_url in com_urls:
            yield response.follow(com_url, callback=self.parse_company)

        # next_page
        next_page = response.css('li.bk a::attr(href)').extract()[-1]
        self.log('next_page: %s' % next_page)
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_company(self, response):
        company = response.css('div.tCompany_center')

        header = company.css('div.tHeader')
        company_name = header.css('h1::attr(title)').extract_first()

        content = header.css('p.ltype::text').extract_first()
        company_type = ''
        company_employers = ''
        company_industry = ''
        if content:
            content_list = content.split('|')
            for content_item in content_list:
                stripped_content = content_item.strip()
                if stripped_content in self.company_types:
                    company_type = stripped_content
                elif re.match('.*[\d]+人', stripped_content) is not None:
                    company_employers = stripped_content
                else:
                    company_industry = stripped_content

        body = company.css('div.tCompany_full')
        company_introduction = body.css('div.con_txt::text').extract_first()
        addresses = body.css('div.bmsg div.inbox p.fp')
        try:
            company_address_nodes = addresses[0].css('::text').extract()
            company_address = company_address_nodes[-1] if company_address_nodes else ''
        except Exception:
            company_address = ''

        company_website = ''
        if len(addresses) > 1:
            company_website = addresses[1].css('a::attr(href)').extract_first()

        yield {
            'name': company_name.strip(),
            'type': company_type.strip(),
            'employers_count': company_employers.strip(),
            'industry': company_industry.strip(),
            'address': company_address.strip(),
            'website': company_website.strip(),
            'introduction': company_introduction.strip()
        }
