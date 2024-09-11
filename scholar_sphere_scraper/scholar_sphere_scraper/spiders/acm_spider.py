import scrapy
from urllib.parse import urlencode

count = 1


class ACMScraper(scrapy.Spider):
    name = 'acm_spider'
    base_url = 'https://dl.acm.org/action/doSearch?'

    default_search_term = 'Abhay Bansal'

    def start_requests(self):
        search_term = getattr(self, 'search_term', self.default_search_term)
        query_params = {
            'AllField': search_term,
            'pageSize': 50
        }
        search_url = f"{self.base_url}{urlencode(query_params)}"
        yield scrapy.Request(url=search_url, callback=self.parse)
    def parse(self, response):
        global count
        issue_items = response.css('div.issue-item__content')
        for item in issue_items:
            title_element = item.css('.issue-item__title a')
            title = " ".join(title_element.xpath('.//text()').getall()).strip()
            link = title_element.attrib['href']

            details = item.css('.epub-section__title::text').get()
            abstract = item.css('.issue-item__abstract p::text').get()
            citations = item.css('.citation span::text').get()

            author_elements = item.css('.hlFld-ContribAuthor a')
            authors_info = []
            for author in author_elements:
                author_name = author.css('::text').get()
                author_profile_link = ("https://dl.acm.org"+author.attrib['href'])
                authors_info.append((author_name, author_profile_link))

            yield {
                'count': count,
                'title': title,
                'link': response.urljoin(link),
                'details': details,
                'abstract': abstract,
                'citations': citations,
                'authors_info': authors_info
            }
            count += 1
        next_page = response.css('a.pagination__btn--next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)
