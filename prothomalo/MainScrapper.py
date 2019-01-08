#----------------------------
#        PROTHOM ALO SCRAPING
#----------------------------

from concurrent import futures
import time

from webscrap import wlog
from webscrap import wscrap

wlog.set_custom_log_info('html/error.log')


categories = "bangladesh international economy opinion sports entertainment" \
             " technology life-style education art-and-literature pachmisheli".split()

MAX_THREAD = 50


def call_cons(category):
    news_scrap = wscrap.NewsScraper(category, wlog)

    news_scrap.retrieve_webpage()
    # news_scrap.write_webpage_as_html()
    # news_scrap.read_webpage_from_html()
    news_scrap.convert_data_to_bs4()
    # news_scrap.print_data()
    news_scrap.parse_soup_to_simple_html()



def scrap_all(categories):
    threads = min(MAX_THREAD, len(categories))

    with futures.ThreadPoolExecutor(threads) as executor:
        response = executor.map(call_cons, categories)

    return len(list(response))



def main(func):
    time_start = time.time()
    count = func(categories)
    time_end = time.time()

    duration = time_end - time_start
    min = int(duration / 60)
    sec = int(duration % 60)
    print(f"\n{count} category fetched in {min} minute(s) {sec} second(s).")



# # entry point
if __name__ == '__main__':
    main(scrap_all)
