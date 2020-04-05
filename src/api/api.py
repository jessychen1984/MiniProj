from flask import request, Flask
from miniproj import calculator, poem
import json

app = Flask(__name__)
logger = app.logger

@app.route('/calculator', methods=['POST'])
def calculator_p():
    logger.info("in calculator")
    print("in calculator")
    data = json.loads(request.get_data())
    limit = int(data['limit'])
    op_count = int(data['op_count'])
    op_type = (data['op_type']).split(",")
    total = int(data['total'])
    logger.info("finish calculator")
    print("finish calculator")
    return calculator.auto_cal_generator(limit, op_count, op_type, total)

@app.route('/poem', methods=['POST'])
def poem_p():
    logger.info("in poem")
    print("in poem")
    data = json.loads(request.get_data())
    ptype = data['type'] if 'type' in data else ""
    index = json.dumps(data['index'], ensure_ascii=False) if 'index' in data else "{}"
    count = int(data['count']) if 'count' in data else 5
    logger.info("finish poem")
    print("finish poem")
    return poem.get_poem(ptype, index, count)
