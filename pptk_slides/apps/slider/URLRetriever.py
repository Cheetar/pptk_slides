#!/usr/bin/env python3

# Retrieves images from Google Images for many randomly chosen queries.
# The folder ./results must exist - this is the destination directory for the downloads
# The wordlist from which the words are chosen must be in ./words.txt

#import asyncio
import imghdr
import os
import random
import shutil
import string
#import sys
import time
#from contextlib import closing
from hashlib import md5
from queue import Queue
from threading import Thread
from urllib import parse

#import aiohttp
import requests

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from util import is_image_funny

#import tqdm


class URLRetriever:

    def __init__(self, dictionary_path=None, download_folder="./"):
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36")
        self.driver = webdriver.PhantomJS(desired_capabilities=dcap)
        self.driver.set_window_size(1120, 550)
        self.dictionary_path = dictionary_path
        self.download_folder = download_folder

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print("URLRetriever failed")
        self.driver.quit()

    def clear_session(self):
        self.driver.getSessionStorage().clear()
        self.driver.getLocalStorage().clear()
        self.driver.delete_all_cookies()

    def get_urls_and_ranks(self, query, limit, depth=0):
        # self.clear_session()
        try:
            self.driver.get("https://images.google.com/")

            self.driver.find_element_by_id("lst-ib").send_keys(query + "\n")

            source = self.driver.page_source
            urls = [
                parse.unquote(
                    entry.split("imgurl=")[1].split("&amp")[0]) for entry in
                ("\n".join([entry for entry in source.split('"') if "imgres?imgurl" in entry])).split(';') if
                "imgurl" in entry][:limit]

            # self.driver.quit()
            # self.__init__()
            return list(enumerate(urls))
        except:
            if(depth == 3):
                return []
            print("URLRetriever failed.")
            self.driver.quit()
            self.__init__(download_folder=self.download_folder, dictionary_path=self.dictionary_path)
            return self.get_urls_and_ranks(query, limit, depth + 1)

    def download_funny(self, no_images):
        with open(self.dictionary_path, 'r') as f:
            dictionary = f.read().split('\n')

        url_queue = Queue(maxsize=0)
        word_queue = Queue(maxsize=0)

        images_workers = [Thread(target=URLRetriever.process_url, args=(
            url_queue, self.download_folder,)) for _ in range(25)]
        for worker in images_workers:
            worker.setDaemon(True)
            worker.start()

        url_workers = [Thread(target=URLRetriever.retrieve_url, args=(word_queue, url_queue,)) for _ in range(10)]
        for worker in url_workers:
            worker.setDaemon(True)
            worker.start()

        print("URLRetriever searching images")
        to_fetch = [random.choice(dictionary) for _ in range(no_images)]

        for query in to_fetch:
            word_queue.put(query)

        word_queue.join()
        url_queue.join()
        print("URLRetriever finished")

    def process_url(url_queue, download_folder):
        while True:
            job = url_queue.get()
            query = job[2]
            url = job[1]
            position = job[0]

            with requests.Session() as ses:
                try:
                    r = ses.get(url, stream=True)
                except Exception as ex:
                    print(ex)
                    pass
                if r.status_code == 200:
                    r.raw.decode_content = True

                    # create random filename
                    length = 10
                    file_string = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))
                    filename = "/tmp/%s" % format(file_string)
                    try:
                        with open(filename, 'wb') as file:
                            for chunk in r.iter_content(chunk_size=1024):
                                if chunk:  # filter out keep-alive new chunks
                                    file.write(chunk)

                        # analyze
                        if os.path.isfile(filename):
                            extension = imghdr.what(filename)
                            if (extension is not None) and (not 'gif' == extension):
                                if is_image_funny(filename):
                                    hash = md5(open(filename, 'rb').read()).hexdigest()
                                    shutil.move(filename, os.path.join(download_folder, "%s-%05d-%s.%s" %
                                                                       (query, position, hash, extension)))
                    except:
                        pass
                    finally:
                        if os.path.isfile(filename):
                            os.remove(filename)

            url_queue.task_done()

    def retrieve_url(word_queue, url_queue):
        with URLRetriever() as scraper:
            while True:
                query = word_queue.get()

                batch = scraper.get_urls_and_ranks(query, 1)
                for entry in batch:
                    url_queue.put((entry[0], entry[1], query))
                time.sleep(random.random() / 5)

                word_queue.task_done()


def main():
    retr = URLRetriever(dictionary_path="./words.txt", download_folder="./tmp/")
    retr.download_funny(1000)
