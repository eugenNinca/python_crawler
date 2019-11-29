from utils import *
import requests
from urllib import parse
from bs4 import BeautifulSoup


class Spider():
    project_name = ''
    base_url = ''
    domain_name = ''
    to_crawl = set()
    crawled = set()

    def __init__(self, project_name, base_url, domain_name):
        Spider.project_name = project_name
        Spider.base_url = base_url
        Spider.domain_name = domain_name

        Spider.to_crawl.add(Spider.base_url)
        # the first instance
        self.create_dir()
        self.crawl_page('Initial spider', Spider.base_url)


    @staticmethod
    def create_dir():
        # create the project directory
        create_website_dir(Spider.project_name)


    @staticmethod
    def crawl_page(thread_name, page_url):
        if page_url not in Spider.crawled:
            print('The thread is ' + thread_name + ' | ' + page_url)
            x = Spider.get_page_links(page_url)

            Spider.set_links_to_crawl(x)

            Spider.to_crawl.remove(page_url)
            # print('To Crawl: ', Spyder.to_crawl)
            Spider.crawled.add(page_url)
            # print('Crawled: ', Spyder.crawled)

    @staticmethod
    def get_page_links(page_url):
        page_links = set()
        try:
            response = requests.get(page_url)
            # check headers response.headers
            if response.status_code == 200:
                html_content = response.content

                bs = BeautifulSoup(html_content, 'html.parser')

                for url in bs.find_all("a", href=True):
                    u = parse.urljoin(Spider.base_url, url['href'])
                    page_links.add(u)

                    # url to file path
                    url['href'] = 'file://'+url_to_file_path(u, Spider.project_name, Spider.base_url)

                content = bs.prettify()

                if page_url == Spider.base_url:
                    file_path = os.path.join(os.getcwd(), Spider.project_name, 'index.html')
                    write_file(file_path, content)
                else:
                    file_path = url_to_file_path(page_url, Spider.project_name, Spider.base_url)
                    write_file(file_path, content)

            return page_links
        except:
            print('Error crawling page ' + page_url)
            return set()

    @staticmethod
    def set_links_to_crawl(links):
        for url in links:
            if url in Spider.to_crawl:
                continue
            if url in Spider.crawled:
                continue
             #  Check if in domain
            if Spider.domain_name not in url:
                continue
            Spider.to_crawl.add(url)

    @staticmethod
    def get_links_to_crawl():
        return Spider.to_crawl
