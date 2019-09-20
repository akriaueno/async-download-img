import asyncio
import re
import time
import requests
from bs4 import BeautifulSoup


async def async_download_img(urls):
    try:
        for url in urls:
            r = requests.get(url)
            file_name = url.split('/')[-1]
            file_path = f'async_{file_name}'
            with open(file_path, 'wb') as f:
                f.write(r.content)
    except Exception:
        pass


def download_img(urls):
    try:
        for url in urls:
            r = requests.get(url)
            file_name = url.split('/')[-1]
            file_path = f'normal_{file_name}'
            with open(file_path, 'wb') as f:
                f.write(r.content)
    except Exception:
        pass

def get_img_list(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    img_srcs = [img['src'] for img in soup.find_all('img')]
    return format_img_srcs(img_srcs, url)


def format_img_srcs(img_srcs, url):
    regex = r'^http'
    pattern = re.compile(regex)
    url = url[:-1] if url[-1] == '/' else url
    return [img_src if pattern.match(img_src) else f'{url}{img_src}' for img_src in img_srcs]

            
if __name__ == '__main__':
    img_list = get_img_list('https://news.google.com/')
    print(img_list)
    print(f'{len(img_list)} files will be downloaded')
    print('continue ? [Y/n]')
    if input() in ['Y', 'y']:
        loop = asyncio.get_event_loop()
        async_start = time.time()
        loop.run_until_complete(async_download_img(img_list))
        async_elapsed_time = time.time() - async_start
        normal_start = time.time()
        download_img(img_list)
        normal_elapsed_time = time.time() - normal_start
        print(f'async: {async_elapsed_time}[s]')
        print(f'normal: {normal_elapsed_time}[s]')
