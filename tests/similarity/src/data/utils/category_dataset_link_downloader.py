import os
import random
import shutil
import time
from pathlib import Path
import os.path as path
import numpy as np
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd

from tests.similarity.src.data.utils.undedected_chrome_driver_with_perfs import ChromeWithPrefs


class CategoryDatasetLinkDownloader:
    def __init__(self, dir_name):
        self.driver = None  # webdriver.Firefox()
        self.df = None
        self.delay = 3
        self.categories_list = []
        self.base_url = "https://www.sciencedirect.com"
        self.dir_name = dir_name
        self.download_dir = self.check_for_download_dir_and_create(dir_name)

    def open_website(self):
        self.driver = webdriver.Firefox()
        self.driver.get("https://www.sciencedirect.com/browse/journals-and-books")

    def check_for_download_dir_and_create(self, dir_name):
        Path("../../data/raw/" + dir_name).mkdir(parents=True, exist_ok=True)
        if path.exists("../../data/raw/" + dir_name + '/categories.csv'):
            self.df = pd.read_csv("../../data/raw/" + dir_name + '/categories.csv')
        else:
            self.df = pd.DataFrame(columns = ["Name", "Category", "URL"])
        return Path("../../data/raw/" + dir_name)

    def save_df(self):
        self.df.to_csv("../../data/raw/" + self.dir_name + '/categories.csv')

    def wait_for_element_to_load(self, type_, feature, driver=None):
        if driver is None:
            driver = self.driver
        try:
            WebDriverWait(driver, self.delay). \
                until(EC.presence_of_element_located((type_, feature)))
        except TimeoutException:
            return TimeoutError

    def open_acces_and_journals(self):
        self.wait_for_element_to_load(By.ID, 'JL')
        element = self.driver.find_element(By.ID, "JL")
        self.driver.execute_script("arguments[0].click();", element)
        element = self.driver.find_element(By.ID, "openAccess")
        self.driver.execute_script("arguments[0].click();", element)

    def get_number(self, text):
        return [int(s) for s in text.replace(',', '').split() if s.isdigit()][0]

    def get_categories(self):
        self.open_website()
        self.open_acces_and_journals()
        categories = self.driver.find_elements(
            By.XPATH, "//li[@class='option-item u-margin-s-left']")
        for i in categories:
            tmp = i.find_elements(By.CLASS_NAME, "options-item-text")
            self.categories_list.append(tmp[0].get_attribute("textContent"))
        self.driver.close()

    def draw_journals_numbers(self, journals_numbers, sample_size):
        indexes = range(0, journals_numbers - 1)
        number_of_downloaded_articles = 0
        while number_of_downloaded_articles < sample_size:
            li = list(np.random.randint(journals_numbers - 1, size=1))
            li.sort()
            if self.go_to_journal_and_take_article(li):
                number_of_downloaded_articles += 1

    def take_article_from_journal(self, driver):
        self.wait_for_element_to_load(By.XPATH,
                                      "//a[@class='anchor js-issue-item-link text-m anchor-default']")
        volumes = driver.find_elements(By.XPATH,
                                       "//a[@class='anchor js-issue-item-link text-m anchor-default']")
        try:
            volume = random.sample(volumes, 1)
            vol_url = volume[0].get_attribute("href")

        except ValueError:
            return False
        volume = driver.get(vol_url)
        articles = driver.find_elements(By.XPATH,
                                        "//a[@class='anchor article-content-title u-margin-xs-top u-margin-s-bottom anchor-default']")
        try:
            article = random.sample(articles[2:], 1)[0]
            url = article.get_attribute("href")
            driver.get(url)
            self.wait_for_element_to_load(By.XPATH,
                                          "//a[@class='link-button accessbar-utility-component "
                                          "accessbar-utility-link link-button-primary']")
            url = driver.find_elements(By.XPATH,
                                       "//a[@class='link-button accessbar-utility-component "
                                       "accessbar-utility-link link-button-primary']"
                                       )
            if len(url) > 0:
                url = url[0].get_attribute("href")
                print(url)
            else:
                driver.close()
                return False

            url = url

        except ValueError:
            return False

        print(url)
        indx = [i for i in range(len(url)) if url.startswith('=', i)][-1]
        row = [url[indx+1:], self.curr_category_name, url]
        self.df.loc[self.df.index.max() + 1] = row
        return True


    def go_to_journal_and_take_article(self, li):
        self.wait_for_element_to_load(By.XPATH,
                                      "//a[@class='anchor js-publication-title "
                                      "anchor-default']")
        journals = self.driver.find_elements(By.XPATH, "//a[@class='anchor js-publication-title anchor-default']")

        if len(journals) <= li[-1]:
            next_button = self.driver.find_elements(By.XPATH,
                                                    "//button[@class='button-alternative button-alternative-secondary "
                                                    "medium-alternative']")[1]
        else:
            next_button = None
        for i in li:
            if i >= len(journals):
                self.driver.execute_script("arguments[0].click();", next_button)
                self.wait_for_element_to_load(By.XPATH,
                                              "//a[@class='anchor js-publication-title "
                                              "anchor-default']")
                journals += self.driver.find_elements(By.XPATH,
                                                      "//a[@class='anchor js-publication-title "
                                                      "anchor-default']")

            url = journals[i].get_attribute("href")
            driver = webdriver.Firefox()
            driver.get(url + "/issues")
            if not self.take_article_from_journal(driver):
                return False
            driver.close()
            return True

    def sample_from_category(self, category_name, sample_size):
        self.curr_category_name = category_name
        self.open_website()
        self.open_acces_and_journals()
        categories = self.driver.find_elements(
            By.XPATH, "//li[@class='option-item u-margin-s-left']")

        old_text = self.driver.find_element(
            By.XPATH, "//h1[@class='u-margin-xxl-top-from-lg "
                      "u-margin-s-bottom-from-lg u-margin-l-top u-margin-s-bottom']") \
            .get_attribute("textContent")
        number_of_articles_old = self.get_number(self.driver.find_element(
            By.XPATH, "//h1[@class='u-margin-xxl-top-from-lg "
                      "u-margin-s-bottom-from-lg u-margin-l-top u-margin-s-bottom']").
                                                 get_attribute("textContent"))
        for i in categories:
            tmp = i.find_elements(By.CLASS_NAME, "options-item-text")
            if tmp[0].get_attribute("textContent") == category_name:
                self.driver.execute_script("arguments[0].click();", tmp[0])

        EC.all_of(
            self.driver.find_element(
                By.XPATH, "//h1[@class='u-margin-xxl-top-from-lg "
                          "u-margin-s-bottom-from-lg u-margin-l-top u-margin-s-bottom']")
            .get_attribute("textContent") != old_text
        )
        self.wait_for_element_to_load(By.XPATH,
                                      "//h1[@class='u-margin-xxl-top-from-lg "
                                      "u-margin-s-bottom-from-lg u-margin-l-top u-margin-s-bottom']"
                                      )
        number_of_articles = number_of_articles_old
        while number_of_articles == number_of_articles_old:
            time.sleep(1)
            number_of_articles = self.get_number(self.driver.find_element(
                By.XPATH, "//h1[@class='u-margin-xxl-top-from-lg "
                          "u-margin-s-bottom-from-lg u-margin-l-top u-margin-s-bottom']").
                                                 get_attribute("textContent"))
        print(number_of_articles)

        self.draw_journals_numbers(number_of_articles, sample_size)
        self.driver.close()
        self.save_df()
