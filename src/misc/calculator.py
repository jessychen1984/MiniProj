'''
A simple python calculation question generator
usg: python calculator.py -d "+,-" -c 3 -l 200 -t 30
usg: python calculator.py --op_type="+,-" --op_count=3 --limit=20 --total=30
'''
import sys, getopt, random

def auto_cal_generator(limit=100, op_count=1, op_type=["+"], total=100):
    print("Here are today's %d works, good luck!" % total)
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
                print("operator error: %s" % op)
                sys.exit(1)
            question = "%s%d" % (question, num)
        print("%d: %s=" % (j+1, question))

def main(argv=None):
    if argv is None:
        argv = sys.argv
    opts, _dummy = getopt.getopt( sys.argv[1:], "l:c:d:t:", ["limit=","op_count=","op_type=","total="])
    limit = 100
    op_count = 1
    op_type = ["+"]
    total = 100
    for opt,arg in opts:
        if opt in ["-l", "--limit"]:
            limit = int(arg)
        elif opt in ["-c", "--op_count"]:
            op_count = int(arg)
        elif opt in ["-d", "--op_type"]:
            op_type = arg.strip().split(",")
        elif opt in ["-t", "--total"]:
            total = int(arg)

    auto_cal_generator(limit, op_count, op_type, total)


if __name__ == '__main__':
    main()
