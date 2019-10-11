# -*- coding: utf-8 -*-

import os
from pymongo import MongoClient

mongo = MongoClient()
db = mongo['jinyong']['xiaoshuo']
dirname = "F:/jinyong/data/books"

for book_obj in db.find():
    print("start to process {}...".format(book_obj["book_name"]))

    book_dir = os.path.join(dirname, book_obj["book_name"]+".txt")
    os.makedirs(book_dir, exist_ok=True)

    for chapter in book_obj["chapters"]:
        chapter_fname = os.path.join(book_dir, chapter['name'])
        with open(chapter_fname, "w", encoding="utf-8") as wf:
            wf.writelines(chapter['content'] + "\n")