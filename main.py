import requests
from bs4 import BeautifulSoup as bs
import asyncio
import aiohttp
import time
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator
from datetime import datetime

my_info = {
    'Name': 'Brandon Harding',
    'Email': 'bharding80@gmail.com'
}



# Tutorials: https://oxylabs.io/blog/asynchronous-web-scraping-python-aiohttp
#            https://www.twilio.com/blog/asynchronous-http-requests-in-python-with-aiohttp

# start_time = time.time()

# async def get_data(session, page):
#     async with session.get(page) as resp:

#         print('I received a page!')

#         # whenever the response comes back, do all of this:
#         data = await resp.text()
#         # this 'data' variable contains the html content (the response) 
#         # of a page in text format
#         soup = bs(data, 'html.parser')

#         print('I parsed the page contents!')

#         # make a list of all the tr tags on that page
#         stock_table = soup.find('table', class_='tabMini tabQuotes')
#         print('I found a table!')


#         tr_tag_list = stock_table.find_all('tr')

#         print('I found some tr tags!')


        
#         data_list = []
#         # find all the td tags in each row
#         for each_tr_tag in tr_tag_list[1:]:
#             td_tag_list = each_tr_tag.find_all('td')

#             row_values = []
#             for each_td_tag in td_tag_list[0:7]:
#                 new_value = each_td_tag.text.strip()
#                 row_values.append(new_value)
            
#             data_list.append(row_values)

#     return data_list
#         # send 'data_list' back to the caller function


# async def main():

#     async with aiohttp.ClientSession() as session:

#         pages = []
#         for page_number in range(1, 50):
#             # https://www.centralcharts.com/en/price-list-ranking/ALL/asc/ts_19-us-nasdaq-stocks--qc_1-alphabetical-order?p=1
#             url_start = 'https://www.centralcharts.com/en/price-list-ranking/'
#             url_end = 'ALL/asc/ts_19-us-nasdaq-stocks--qc_1-alphabetical-order?p='
#             url = url_start + url_end + str(page_number)
#             pages.append(url)

#         # take a bunch of tasks and shove them into a list. This list is then 
#         # sent to the 'get_data' function above. That function sends back 'data_list'.
#         tasks = []
#         for page in pages:
#             tasks.append(asyncio.ensure_future(get_data(session, page)))
#             # go do the 'get_data' function

#         print('I compiled all your tasks!')





#         # data is what is returned from the 'get_data' function above        
#         data = await asyncio.gather(*tasks)

#         print('test 2')

#         # x is a list containing lists of tds, one for each tr on that page
#         final_list = []
#         for page in data:
#             for tr in page:
#                 final_list.append(tr)

#         print(final_list)

# asyncio.run(main())
# print("--- %s seconds ---" % (time.time() - start_time))








async def fetch_page(session, url):
    print('I sent a request to the server')
    async with session.get(url) as response:
        print('I received a response from the server!')
        return await response.text()
        # return the response to the calling function below


async def scrape_multiple_pages(urls):
    async with aiohttp.ClientSession() as session:

        print('Now that I have all the urls, I will create a list of tasks')
        tasks = [asyncio.create_task(fetch_page(session, url)) for url in urls]
        print('I created my list of tasks')
        # sends the task list to the 'fetch_page' function


        # returns a list of the results of each task and saves it as 'pages'
        pages = await asyncio.gather(*tasks)
        print("I received all the results from the 'fetch_page' function")
        # take the results and exit this function
        return pages



start_time = time.time()

urls = []
for page_number in range(1, 10):
    # https://www.centralcharts.com/en/price-list-ranking/ALL/asc/ts_19-us-nasdaq-stocks--qc_1-alphabetical-order?p=1
    url_start = 'https://www.centralcharts.com/en/price-list-ranking/'
    url_end = 'ALL/asc/ts_19-us-nasdaq-stocks--qc_1-alphabetical-order?p='
    url = url_start + url_end + str(page_number)
    urls.append(url)
print('Collected all urls!')


# receive the 'pages' variable from the function above
# 'pages' is a list of the html content
pages = asyncio.run(scrape_multiple_pages(urls))

new_list = ''.join(pages)
soup = bs(new_list, 'html.parser')
tables = soup.find_all('table')

header_tag_list = tables[0].find_all('th')
header_list = []
for tag in header_tag_list[0:7]:
    title = tag.text
    header_list.append(title)
print(header_list)

top_list = []
for table in tables:
    rows = table.find_all('tr')

    # for each row except the header row
    for row in rows[1:]:
        row_list = []
        cells = row.find_all('td')
        # one list per row, each list containing the td tags for that row

        for cell in cells[0:7]:
            new_value = cell.text.strip()
            row_list.append(new_value)
        top_list.append(row_list)

print(top_list)        
print("--- %s seconds ---" % (time.time() - start_time))































# Compare speed to the synchronous code:

# start_time = time.time()

# pages = []
# for page_number in range(1, 5):
#     # https://www.centralcharts.com/en/price-list-ranking/ALL/asc/ts_19-us-nasdaq-stocks--qc_1-alphabetical-order?p=1
#     url_start = 'https://www.centralcharts.com/en/price-list-ranking/'
#     url_end = 'ALL/asc/ts_19-us-nasdaq-stocks--qc_1-alphabetical-order?p='
#     url = url_start + url_end + str(page_number)
#     pages.append(url)

# for page in pages:
#     response = requests.get(page)
#     soup = bs(response.text, 'html.parser')

#     # Find the table and the tr tags in it
#     stock_table = soup.find('table', class_='tabMini tabQuotes')
#     tr_tag_list = stock_table.find_all('tr')

#     data_list = []
#     # find all the td tags in each row
#     for each_tr_tag in tr_tag_list[1:]:
#         td_tag_list = each_tr_tag.find_all('td')

#         row_values = []
#         for each_td_tag in td_tag_list[0:7]:
#             new_value = each_td_tag.text.strip()
#             row_values.append(new_value)
#         data_list.append(row_values)


# print(data_list)
# print("--- %s seconds ---" % (time.time() - start_time))







