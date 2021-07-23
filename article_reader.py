#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from article import Article
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class ArticleReader:
    def __init__(self, chromedriver, url):
        options = Options()
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(chromedriver, chrome_options=options)
        self.driver.get(url)
        self.articles = []

    def __del__(self):
        self.driver.close()

    def get_all_articles(self):
        morePages = True
        while morePages:
            self.articles.extend([article for article in self.__get_page_articles()])
            morePages = self.__next_page()
        self.sort_articles()
        return self.articles

    def sort_articles(self):
        self.articles.sort(key=lambda article: article.publishedDate)
        self.articles.sort(key=lambda article: article.name)

    def __get_page_articles(self):
        articleElements = self.driver.find_elements_by_tag_name('article')
        for articleElement in articleElements:
            firstName = articleElement.find_element_by_css_selector(
                "meta[itemprop='givenName']").get_attribute("content")
            surname = articleElement.find_element_by_css_selector(
                "meta[itemprop='familyName']").get_attribute("content")
            publishedDate = articleElement.find_element_by_css_selector(
                "meta[itemprop='datePublished']").get_attribute("content")
            title = articleElement.find_element_by_css_selector(
                "h3[itemprop='name headline']").get_attribute("innerHTML")
            link = articleElement.find_element_by_tag_name(
                "article>a").get_attribute("href")
            yield Article(firstName, surname, publishedDate, title, link)

    def __next_page(self):
        nextPageElements = self.driver.find_elements_by_xpath(
            "/html/body/main/div[2]/div/div/aside[2]/p[3]/a")
        if len(nextPageElements) > 0:
            nextPageElements[0].click()
            return True
        else:
            return False