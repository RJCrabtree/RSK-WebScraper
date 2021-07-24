#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from article_writer import ArticleWriter
from article_reader import ArticleReader


def main():
    article_reader = ArticleReader(
        "./chromedriver", "https://www.identityserver.com/articles")
    article_writer = ArticleWriter(article_reader.get_all_articles())
    article_writer.write("identity_server_articles")


if __name__ == "__main__":
    main()
