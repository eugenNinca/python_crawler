import sys
import time
from utils import *
import threading
from queue import Queue
from spider import Spider

# get url from cmd and the depth
link = input('Please enter a valid URL:')

if valid_url(link):

    home_page = link
    PROJECT_NAME = get_domain(home_page)
    DOMAIN_NAME = get_domain(home_page)

    NUMBER_THREADS = 4

    queue = Queue()

    # The first spider
    Spider(PROJECT_NAME, home_page, DOMAIN_NAME)

    # Check if there are items in the queue, if so crawl them
    def crawl():
        if len(Spider.get_links_to_crawl()) > 0:
            print(str(len(Spider.get_links_to_crawl())) + ' links in the queue!')
            create_jobs()


    # create threads( will die after main exits)
    def create_workers():

        for _ in range(NUMBER_THREADS):
            t = threading.Thread(target=work)
            t.daemon = True
            t.start()


    # Each link is a new job
    def create_jobs():

        for link in Spider.get_links_to_crawl():
            queue.put(link)
        queue.join()


    # do the next job in the queue
    def work():

        while True:
            url = queue.get()
            Spider.crawl_page(threading.current_thread().name, url)
            queue.task_done()

    start = time.time()

    create_workers()
    crawl()

    print('Entire process took: ', time.time() - start)

else:
    print('Not a valid url')
