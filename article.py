#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

class Article:
    def __init__(self, firstName, surname, publishedDate, title, link):
        self.name = f'{firstName} {surname}'
        self.publishedDate = datetime.strptime(publishedDate, "%Y-%m-%d %H:%M:%S")
        self.title = title
        self.link = link