import requests
from bs4 import BeautifulSoup as bs
import asyncio
import aiohttp
import time

# Tutorial: https://oxylabs.io/blog/asynchronous-web-scraping-python-aiohttp


_start = time.time()

async def main():

    pages = []
    for page_number in range(1, 5):
        # https://www.centralcharts.com/en/price-list-ranking/ALL/asc/ts_19-us-nasdaq-stocks--qc_1-alphabetical-order?p=1
        url_start = 'https://www.centralcharts.com/en/price-list-ranking/'
        url_end = 'ALL/asc/ts_19-us-nasdaq-stocks--qc_1-alphabetical-order?p='
        url = url_start + url_end + str(page_number)
        pages.append(url)



    webpage = requests.get(pages[0])
    soup = bs(webpage.text, 'html.parser')
    stock_table = soup.find('table', class_='tabMini tabQuotes')
    th_tag_list = stock_table.find_all('th')

    headers = []
    for each_tag in th_tag_list:
        title = each_tag.text
        headers.append(title)
    headers[0] = 'Name'

    new_headers = []
    for header in headers:
        if header not in ('Cap.', 'Issued Cap.', ''):
            new_headers.append(header)
    headers = new_headers




    async with aiohttp.ClientSession() as session:
        for page in pages:
            async with session.get(page) as response:
                resp = await response.text()

                soup = bs(resp, 'html.parser')

                # Find the table and the tr tags in it
                stock_table = soup.find('table', class_='tabMini tabQuotes')
                tr_tag_list = stock_table.find_all('tr')

                data_list = []
                # find all the td tags in each row
                for each_tr_tag in tr_tag_list[1:]:
                    td_tag_list = each_tr_tag.find_all('td')

                    row_values = []
                    for each_td_tag in td_tag_list[0:7]:
                        new_value = each_td_tag.text.strip()
                        row_values.append(new_value)
                    data_list.append(row_values)

    print(headers)
    print(data_list)

    time_difference = time.time() - _start
    print(time_difference)



asyncio.run(main())



