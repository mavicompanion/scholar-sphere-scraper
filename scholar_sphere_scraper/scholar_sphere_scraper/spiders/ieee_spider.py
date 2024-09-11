import scrapy
from scrapy_splash import SplashRequest
from urllib.parse import urlencode


class IEEESpider(scrapy.Spider):
    name = 'ieee_spider'
    base_url = 'https://ieeexplore.ieee.org/search/searchresult.jsp?'

    default_search_term = 'Abhay Bansal'
    count = 1
    current_page = 1
    custom_settings = {
        'FEEDS': {
            'response.html': {
                'format': 'html',
                'encoding': 'utf8',
            },
        },
    }

    def __init__(self, search_term='', *args, **kwargs):
        super(IEEESpider, self).__init__(*args, **kwargs)
        self.search_term = search_term

    def start_requests(self):
        search_term = getattr(self, 'search_term', self.default_search_term)
        query_params = {
            'queryText': search_term,
            'pageNumber':1
        }
        search_url = f"{self.base_url}{urlencode(query_params)}"

        yield SplashRequest(
            url=search_url,
            callback=self.parse,
            args={'wait': 10, 'timeout': 60},
            splash_headers={'Accept-Language': 'en-US,en;q=0.9','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6446.71 Safari/537.36'}
        )

    def parse(self, response):

        issue_items = response.xpath('//div[contains(@class, "List-results-items")]')
        self.log(f'Found {len(issue_items)} items.')

        if not issue_items:
            self.log('No items found on the page. Check if the XPath selectors are correct.')
            return

        for item in issue_items:
            try:
                title_element = item.xpath('.//h3[contains(@class, "result-item-title")]/a')
                title = title_element.xpath('text()').get(default='No title available').strip()
                link = title_element.xpath('@href').get(default='No link available')

                details = item.xpath('.//div[@class="description"]//div//a/text()').get(
                    default='No details available')
                abstract = item.xpath('.//div[contains(@class, "Abstract-text")]//p/text()').get(
                    default='No abstract available')
                citations = item.xpath(".//div[contains(text(), 'Cited by:')]//span//text()").get(
                    default='No citation count available').split()[1].replace("(","").replace(")","")

                author_elements = item.xpath('.//p[contains(@class, "author")]/span[@class="text-base-md-lh"]/a')
                authors_info = []
                for author in author_elements:
                    author_name = ''.join(author.xpath('.//span//text()').getall()).strip()
                    author_profile_link = response.urljoin(
                        author.xpath('@href').get(default='No profile link available'))
                    authors_info.append((author_name, author_profile_link))

                yield {
                    'count': self.count,
                    'title': title,
                    'link': response.urljoin(link),
                    'details': details,  #
                    'abstract': abstract, #
                    'citations': citations, #
                    'authors_info': authors_info
                }
                self.count += 1
            except Exception as e:
                self.log(f'Error extracting data: {e}')

        next_page_button = response.xpath('//li[contains(@class, "next-btn")]')
        if next_page_button:
            self.current_page += 1
            query_params = {
                'queryText': self.default_search_term,
                'pageNumber': self.current_page
            }
            next_page_url = f"{self.base_url}{urlencode(query_params)}"
            yield SplashRequest(
                url=next_page_url,
                callback=self.parse,
                args={'wait': 10, 'timeout': 60},
                splash_headers={'Accept-Language': 'en-US,en;q=0.9'}
            )
        else:
            self.log('No more pages to follow.')