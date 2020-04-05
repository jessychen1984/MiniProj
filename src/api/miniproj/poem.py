# -*- coding: utf-8 -*-
'''
A simple chinese poem viewer
usg: python poem.py -t "tang" -i '{"author":"李白", "title":"静夜思"}'  -c 2
usg: python poem.py --type="tang" --indexs='{"author":"李白", "title":"静夜思"}' --count=2

poem data from https://github.com/chinese-poetry/chinese-poetry
Chinese tranditional and simple transfer code is from: https://github.com/skydark/nstools/tree/master/zhtools
'''

import sys, getopt, random, subprocess, json, os, pymysql,codecs
from utils import langconv

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

poem_path_prefix = "./data"
poem_type_list = ["tang", "song", "yuan", "shijing"]
traditional_data = ["tang"]
grep_poems = ["tang", "song"]

#index is a dict json str, like: '{"author":"李白", "title":"静夜思"}'
def get_poem(poem_type="", index_json="{}", count=1):
    if not poem_type:
        i = random.randint(1, len(poem_type_list))
        poem_type = poem_type_list(i) 
    poem_type = poem_type.lower()

    indexs = {}
    if poem_type in traditional_data and index_json:
        index_json = convert(index_json, "t")
    if index_json:
        indexs = json.loads(index_json)
    
    poem_list = get_res(poem_type, indexs, count)

    if count <= len(poem_list):
        poem_list = random.sample(poem_list, count)

    if poem_type in traditional_data:
        poem_list = convert_all(poem_list)
    return json.dumps(poem_list, ensure_ascii=False)

def convert(text, tp="s"):
    return langconv.Converter('zh-han%s' % tp).convert(text)

def convert_all(in_obj, tp="s"):
    in_type = type(in_obj)
    if in_type is str:
        return convert(in_obj, tp)

    out_obj = None
    if in_type is list: 
        out_obj=[]
    elif in_type is dict:
        out_obj={}
    else:
        return in_obj

    for obj in in_obj:
        if in_type is list:
            out_obj.append(convert_all(obj, tp))
        elif in_type is dict:
            out_obj[obj] = convert_all(in_obj[obj], tp)

    return out_obj

def get_res(poem_type, indexs, count):
    db = DB()
    sql = "select * from %s" % poem_type
    if not indexs:
        sql_m = "select max(id) as maxid from %s" % poem_type
        mid = db.query(sql_m)
        mid = int(mid[0]['maxid'])
        ids = random.sample(range(1,mid), count)
        sql = "%s where id in (%s)" % (sql, ",".join(list(map(str, ids))))
        return db.query(sql)

    a_condition = []
    c_condition = []
    for i in indexs:
        if i not in ["paragraphs","content"]:
            a_condition.append("%s='%s'" % (i, indexs[i]))
            c_condition.append("%s like '%%%s%%'" % (i, indexs[i]))
            continue
        c_sql = "%s like '%%%s%%'" % (i, indexs[i])
        a_condition.append(c_sql)
        c_condition.append(c_sql)

    a_sql = "%s where %s" % (sql, " and ".join(a_condition))

    res = []
    if a_sql:
        res = db.query(a_sql)
    if not res or len(res)==0:
        c_sql = "%s where %s" % (sql, " and ".join(c_condition))
        res = db.query(c_sql)
    return res

class DB(object):
    def __init__(self):
        self.db = pymysql.connect("localhost","api","qmsjyff","api",charset="utf8",cursorclass = pymysql.cursors.DictCursor)
        self.cursor = self.db.cursor()

    def __del__(self):
        self.db.close()

    def query(self, sql):
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        return data
