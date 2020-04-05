'''
A simple python calculation question generator
usg: python calculator.py -d "+,-" -c 3 -l 200 -t 30
usg: python calculator.py --op_type="+,-" --op_count=3 --limit=20 --total=30
'''
import sys, getopt, random, json

def auto_cal_generator(limit=100, op_count=1, op_type=["+"], total=100):
    res = {}
    if limit>999 or op_count>9 or total>99:
        res["status"] = "failed"
        res["msg"] = "exceed max input limit"
        return json.dumps(res)

    questions = []
    l = len(op_type)-1
    for j in range(0, total):
        up = limit
        question = ""
        for i in range(0, op_count+1):
            num = 0
            if i == 0:
                num = random.randint(1,max(1,min(limit,up))) 
                question = "%s%d" % (question, num)
                up -= num
                continue
            op = "+"
            if limit - up > 0:
                op_i = random.randint(0,l)
                op = op_type[op_i]
            question = "%s%s" % (question, op)
            if op =="+":
                num = random.randint(1,max(1,min(limit,up))) 
                up -= num
            elif op == "-":
                num = random.randint(1,max(limit-up, 1)) 
                up += num
            else:
                res["status"] = "failed"
                res["msg"] = "operator error: %s" % op
                return json.dumps(res)
            question = "%s%d" % (question, num)

        questions.append("%d: %s=" % (j+1, question))

    res["msg"] = "Here are today's %d works, good luck!" % total
    res["questions"] = questions
    res["status"] = "success"
    return json.dumps(res)
