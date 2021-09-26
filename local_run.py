from event_util import *

def make_move(who,where):
    return {"player": who, "action": "putSymbol", "position": where}

def get_board(nw,n,ne,w,c,e,sw,s,se):
    tmp = """
            |{}|{}|{}|
            +--+--+--+
            |{}|{}|{}|
            +--+--+--+
            |{}|{}|{}|
    """
    tmp = tmp.format(nw,n,ne,w,c,e,sw,s,se)
    return tmp
def run_first(pre_seq):
    events = []
    while True:
        if len(events)%2 == 0:
            side,region = move_algo(events,'O')
            print(side,region)
            events.append(make_move(side,region))
            cur_broad = get_cur_borad(events)
            print('cur',cur_broad)
            r = get_board(
                cur_broad['NW'],
                cur_broad['N'],
                cur_broad['NE'],
                cur_broad['W'],
                cur_broad['C'],
                cur_broad['E'],
                cur_broad['SW'],
                cur_broad['S'],
                cur_broad['SE'],

            )
            print('-'*10)
            print(r)
        else:
            print('-' * 10)
            # player
            tmp = """
                    |NW|N |NE|
                    +--+--+--+
                    |W |C |E |
                    +--+--+--+
                    |SW|S |SE|
            """


            print(tmp)
            if len(pre_seq)>0:
                events.append(make_move('X', pre_seq[0]))
                pre_seq = pre_seq[1:]

            else:
                region = input("where ?")
                events.append(make_move('X', region))

run_first(['SE','SW'])