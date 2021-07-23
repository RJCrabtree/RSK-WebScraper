#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import List
from article import Article
import xlwt


class ArticleWriter:
    def __init__(self, articles):
        self.articles = articles

    def write(self, filename: str):
        wb = xlwt.Workbook()
        sh = wb.add_sheet(filename.replace('_', ' '))
        self.__write_header(sh)
        for row, article in enumerate(self.articles):
            self.__write_article_row(sh, row+1, article)
        wb.save(f"{filename}.xls")

    def __write_article_row(self, sh: xlwt.Workbook, row, article: Article):
        dateStyle = xlwt.XFStyle()
        dateStyle.num_format_str = 'DD/MM/YYYY'
        sh.write(row, 0, article.name)
        sh.write(row, 1, article.publishedDate, dateStyle)
        sh.write(row, 2, article.title)
        sh.write(row, 3, article.link)

    def __write_header(self, sh: xlwt.Workbook):
        sh.write(0, 0, "Name")
        sh.write(0, 1, "Published Date")
        sh.write(0, 2, "Title")
        sh.write(0, 3, "Link")