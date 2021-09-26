import requests
from flask import Flask
from flask import request,jsonify
app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"
"""
{
  "battleId": "21083c13-f0c2-4b54-8cb1-090129ffaa93"
}
"""
arenaEndpoint = ""
events = []
info = {
    'my_side':'',
    'battleId':'',
}
from event_util import get_event_type,move_algo,check_move_event
@app.route('/tic-tac-toe', methods=['POST'])
def start():
    """
    http://127.0.0.1:5000/find?city=shenzhen
    :return:
    """
    param = request.json # 如果不行换下面的param
    #param = request.args
    t = get_event_type(param)
    if t:
        if t== 'start':
            battleId = param.get('battleId', '')
            info['battleId'] =battleId
            events.append(param)
            if battleId != '':
                # Your system initiates a GET request at {arenaEndpoint}/tic-tac-toe/start/{battleId}
                url = f"{arenaEndpoint}/tic-tac-toe/start/{battleId}"
                requests.get(url)
                return jsonify({'res':'success'})

        elif t == 'initial':
            info['my_side'] = param.get('youAre', '')
            events.append(param)
        elif t == 'move':
            battleId = info['battleId']
            if not check_move_event(events):
                # flip
                url = f'{arenaEndpoint}/tic-tac-toe/play/{battleId}'
                request.post(url, json={  "action": "(╯°□°)╯︵ ┻━┻"})
            side, region = move_algo(events, info['my_side'])

            data ={
              "action": "putSymbol",
              "position": region
            }
            url =f'{arenaEndpoint}/tic-tac-toe/play/{battleId}'
            request.post(url,json = data)

            events.append(param)

    a = int()
    b = int(request.args.get('b', 1))
    return jsonify({'res':a+b})



@app.route('/addition', methods=['POST'])
def add():
    """
    http://127.0.0.1:5000/find?city=shenzhen
    :return:
    """
    # a = int(request.args.get('a', 0))
    # b = int(request.args.get('b', 0))
    param = request.json # res = requests.post('http://127.0.0.1:5000/addition',json={'a':1,'b':2}) 对应
    print(param)
    return jsonify({'res':param['a']+param['b']})

if __name__ == '__main__':
    app.run(debug=True)
