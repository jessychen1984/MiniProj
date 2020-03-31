# -*- coding: utf-8 -*-
'''
A simple chinese poem viewer
usg: python poem.py -t "tang" -i '{"author":"李白", "title":"静夜思"}'  -c 2
usg: python poem.py --type="tang" --indexs='{"author":"李白", "title":"静夜思"}' --count=2

poem data from https://github.com/chinese-poetry/chinese-poetry
Chinese tranditional and simple transfer code is from: https://github.com/skydark/nstools/tree/master/zhtools
'''

import sys, getopt, random, subprocess, json, os
from langconv import *


poem_path_prefix = "./data"
poem_type_list = ["tang", "song", "yuan", "shijing"]
traditional_data = ["tang"]
grep_poems = ["tang", "song"]

#index is a dict json str, like: '{"author":"李白", "title":"静夜思"}'
def get_poem(poem_type="", index_json="", count=1):
    if not poem_type:
        i = random.randint(1, len(poem_type_list))
        poem_type = poem_type_list(i) 
    poem_type = poem_type.lower()
    poem_path = "%s/%s" % (poem_path_prefix, poem_type)

    indexs = {}
    if poem_type in traditional_data and index_json:
        index_json = convert(index_json, "t")
    if index_json:
        indexs = json.loads(index_json)

    file_list = []
    if indexs and poem_type in grep_poems:
        for i in indexs:
            grep_cmd = ""
            if not i in ["content", "paragraphs"]:
                grep_cmd = "grep -rl \"\\\"%s\\\".*%s\" %s" % (i, indexs[i], poem_path)
            else:
                grep_cmd = "grep -rl \"%s\" %s" % (indexs[i], poem_path)
            res = subprocess.run(grep_cmd, shell=True, stdout=subprocess.PIPE).stdout.decode()
            file_list = res.strip().split("\n")
            break
    else:
        file_list = os.listdir(poem_path)
        file_list = [os.path.join(poem_path, f) for f in file_list]
    
    poem_list = []
    poem_contain_list = []
    for f in file_list:
        if not f.endswith(".json"):
            continue
        poems = json.load(open(f,"r"))
        if not indexs:
            poem_list.extend(poems)
            continue
        for poem in poems:
            match = is_match(poem, indexs)
            if match == 2:
                poem_list.append(poem)
            elif match == 1:
                poem_contain_list.append(poem)
    
    if count <= len(poem_list):
        poem_list = random.sample(poem_list, count)
    else:
        count -= len(poem_list)
        if count <= len(poem_contain_list):
            poem_list.extend(random.sample(poem_contain_list, count))
        else:
            poem_list.extend(poem_contain_list)

    if poem_type in traditional_data:
        poem_list = convertAll(poem_list)
    return json.dumps(poem_list, ensure_ascii=False)

def is_match_str(query, original):
    if not query in original:
        return 0 
    if query != original:
        return 1
    return 2

#retrun value: 0, no match; 1, contain match; 2, all match
def is_match(poem, indexs):
    match_level_final = 2
    for i in indexs:
        match_level = 0
        if type(poem[i]) is list:
            for p in poem[i]:
                current_level = is_match_str(indexs[i], p)
                match_level = current_level if match_level < current_level else match_level
        else:
            match_level = is_match_str(indexs[i], poem[i])

        if match_level == 0:
            match_level_final = 0
            break
        
        match_level_final = match_level if match_level < match_level_final else match_level_final

    return match_level_final

def convert(text, tp="s"):
    return Converter('zh-han%s' % tp).convert(text)

def convertAll(in_obj, tp="s"):
    in_type = type(in_obj)
    if in_type is str:
        return convert(in_obj, tp)

    out_obj = None
    if in_type is list: 
        out_obj=[]
    elif in_type is dict:
        out_obj={}
    else:
        print("in obj type is not list or dict: %s" % in_type)
        return out_obj

    for obj in in_obj:
        if in_type is list:
            out_obj.append(convertAll(obj, tp))
        elif in_type is dict:
            out_obj[obj] = convertAll(in_obj[obj], tp)

    return out_obj

def main(argv=None):
    if argv is None:
        argv = sys.argv
    opts, _dummy = getopt.getopt( sys.argv[1:], "t:i:c:", ["type=","indexs=","count="])
    poem_type = ""
    indexs = ""
    count = 1
    for opt,arg in opts:
        if opt in ["-t", "--type"]:
            poem_type = arg
        elif opt in ["-i", "--indexs"]:
            indexs = arg
        elif opt in ["-c", "--count"]:
            count = int(arg)
    
    res_poems = get_poem(poem_type, indexs, count)
    print(res_poems)

if __name__ == '__main__':
    main()

