import asyncio
import re
import time
import requests
from bs4 import BeautifulSoup

MAX_CONNECTION = 1


def download_img(url):
    # TODO separete disk I/O from this func
    # ???
    # yeild r.content and push queue
    # pop queue and write files asynchronously
    # Semaphore may be bottleneck
    # ???
    r = requests.get(url, stream=True)
    file_name = url.split('/')[-1]
    file_path = f'async_{file_name}'
    with open(file_path, 'wb') as f: f.write(r.content)


async def async_download_imgs(urls, loop):
    try:
        sem = asyncio.Semaphore(MAX_CONNECTION)

        def async_download_img(url):
            async with sem:
                return loop.run_in_executor(None, download_img, url)

        cors = [async_download_img(url) for url in urls]
        return await asyncio.gather(*cors)
    except Exception:
        pass


def download_imgs(urls):
    try:
        for url in urls:
            download_img(url)
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
    return [img_src if pattern.match(img_src)
            else f'{url}{img_src}' for img_src in img_srcs]


if __name__ == '__main__':
    url = input('URL: ')
    img_list = get_img_list(url)
    print(img_list)
    print(f'{len(img_list)} files will be downloaded')
    print('continue ? [Y/n]')
    if input() in ['Y', 'y']:
        loop = asyncio.get_event_loop()
        start = time.time()
        loop.run_until_complete(async_download_imgs(img_list, loop))
        elapsed_time = time.time() - start
        print(f'async: {elapsed_time}[s]')
        start = time.time()
        download_imgs(img_list)
        elapsed_time = time.time() - start
        print(f'normal: {elapsed_time}[s]')
