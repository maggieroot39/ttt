import logging
import socket
from codeitsuisse import app
logger = logging.getLogger(__name__)

@app.route('/', methods=['GET'])
def default_route():
    return "Python Template"

from event_util import get_event_type,move_algo,check_move_event
"""
{
  "battleId": "21083c13-f0c2-4b54-8cb1-090129ffaa93"
}
"""
arenaEndpoint ="https://cis2021-arena.herokuapp.com"
events = []
info = {
    'my_side':'',
    'battleId':'',
}

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


logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)



if __name__ == "__main__":
    logging.info("Starting application ...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 0))
    port = sock.getsockname()[1]
    sock.close()
    app.run(port=5000)
