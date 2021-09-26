def get_event_type(event):
    """
    判断event 类型
    :param event: 
    :return: 
    """
    #data: {"youAre":"O","id":"15f6301f-cbdd-4084-a810-df2e9c83238f"}
    # data: {"player":"O","action":"putSymbol","position":"NW"}
    # data: {"winner": "draw"}
    # data: {"winner": "O"}
    # {"player":"O","action":"(╯°□°)╯︵ ┻━┻"}
    if len(event.keys()) == 1 and 'battleId' in event:
        return 'start'
    if 'youAre' in event:
        return 'initial'
    elif 'action' in event and event.get('action') == 'putSymbol':
        return 'move'
    elif 'winner' in event:
        return 'end'
    elif 'action' in event and event.get('action') == '(╯°□°)╯︵ ┻━┻':
        return 'flip'
    return None


def get_N_S(cs ):
    """
    输出NS
    :param cs: 
    :return: 
    """
    r =  []
    for c in cs:
        if c in "NS":
            r.append(c)
    return r

def get_W_E(cs ):
    """
    输出WE
    :param cs: 
    :return: 
    """
    r =  []
    for c in cs:
        if c in "WE":
            r.append(c)
    return r

def get_edge_regions():
    """
    得到中间的 位置
    :return: 
    """
    return ['N', 'S', 'E', 'W']

def get_corner_regions():
    """
    角落位置
    :return: 
    """
    return  ['NW','NE','SW','SE']

def get_oppo_corner(region):
    """
    对角
    :param region: 
    :return: 
    """
    cs = get_corner_regions()
    cs_ = [r for r in cs if r[0]!=region[0] and r[1] != region[1]]
    return cs_

def get_neigh_corner(region):
    """
    邻角
    :param region: 
    :return: 
    """
    oppo = get_oppo_corner(region)
    return [ u for u in get_corner_regions() if u not in [oppo,region]]

def get_same_edge(first_move,new_move):
    """
    得到两个邻角的共同 位置  NW ， NE -- N
    :param first_move: 
    :param new_move: 
    :return: 
    """
    edge = ''
    if new_move[0] == first_move[0]:
        edge = new_move[0]
    elif new_move[1] == first_move[1]:
        edge = new_move[1]
    return edge

def get_oppo_map():
    """
    得到相反位置
    :return: 
    """
    oppo_map = {
        'N': 'S',
        'E': 'W',
    }
    more = {v: k for k, v in oppo_map.items()}
    oppo_map.update(more)
    return oppo_map
def check_move_event(events):
    """
    查看合法性，有问题就掀桌
    :param events:
    :return: 是否有问题
    """
    events_ = [e for e in events if get_event_type(e) == 'move']
    moves = [(d['player'], d['position']) for d in events_]
    if len(set(moves))!= len(set([e for player , e in moves])):
        return False
    current_broad = {}

    for k,v in moves:
        if k not in current_broad:
            current_broad[k] = []
        current_broad[k].append(v)
    if abs(len(current_broad['O']) -len(current_broad['X']) )>1:
        return False
    for i in range(len(moves)):
        if i+1 == len(moves):
            return False
        if moves[i][0] == moves[i+1][0]:
            return False
    if moves[-1][0] not in "OX":# 是否输入合法棋子
        return False
    if moves[-1][-1] not in get_all_region():#是否 输入合法位置
        return False
    return True

def get_cur_borad(events):
    """
    本地测试用
    :param events: 
    :return: 
    """
    events_ = [ e for e in events if get_event_type(e) == 'move']
    #{"player":"O","action":"putSymbol","position":"NW"}
    moves = [(d['player'],d['position'] ) for d in events_]
    current_broad = {}
    for player ,reg in moves:
        current_broad[reg] = player
    for reg in get_all_region():

        if reg not in current_broad:
            current_broad[reg] = '  '
        else:
            current_broad[reg] += ' '

    return current_broad

def move_algo(events,my_side):
    """
    ai 下棋算法， 枚举了 先手和 后手的 前两步情况， 
    剩下的情况按照  连3  | 堵对方连3 | 连双2 |堵对方连双2 | 对角下子|NSEW 下子的顺序实现
    :param events: 
    :param my_side: 
    :return: 
    """
    events_ = [ e for e in events if get_event_type(e) == 'move']
    #{"player":"O","action":"putSymbol","position":"NW"}
    moves = [(d['player'],d['position'] ) for d in events_]
    current_broad = {}
    covered_region = [ reg for player, reg in moves]
    for k,v in moves:
        if k not in current_broad:
            current_broad[k] = []
        current_broad[k].append(v)
    if my_side == 'O':# 先手
        if moves == []:
            return ('O','C')
        if len(moves) == 2:
            if moves[0] ==  ('O','C'):
                if moves[1] in [('X','N'),('X','S'),('X','W'),('X','E')]:
                    next_p =  ['NW','SE']
                    next_p = [u for u in next_p if moves[1][1] in u]
                    p = next_p[0]
                    return ('O',p)
                elif moves[1][1] in ['NW','NE','SW','SE']:
                    # if oppo is Nw , my move is SW or NE
                    """
                    |NW|N |NE|
                    +--+--+--+
                    |W |C |E |
                    +--+--+--+
                    |SW|S |SE|

                    """
                    oppo_last = moves[1][1]
                    rs = [ diag for diag in ['NW','NE','SW','SE'] if any([c in diag for c in oppo_last])]
                    r = rs[0]
                    return ('O',r)

        if len(moves) == 4:
            attracks = []
            defence = []
            for region in get_all_region():
                if region in covered_region:
                    #
                    continue
                if region == 'S':
                    print('s')
                win_line = get_win_line(current_broad['O'],region)
                win_line_oppo = get_win_line(current_broad['X'],region)
                print('len = 4 win line')
                if win_line:
                    # 连 3
                    attracks.append(('O',region))
                if win_line_oppo:
                    # 堵住
                    defence.append(('O',region))
                print('current_region',region , defence,attracks)
            if len(attracks)>0:
                return attracks[0]
            elif len(defence)>0:
                return defence[0]
            else:
                diagonal = [reg for reg in current_broad['O'] if len(reg)>1][0]
                mid_oppo = [reg for reg in current_broad['X'] if len(reg)==1]
                if len(mid_oppo) > 0:
                    reg = diagonal.replace(mid_oppo,'')
                    return ('O',reg)
                else:
                    if 'C' not in covered_region:
                        return (my_side, "C")
                    for reg in get_corner_regions():
                        if reg not in covered_region:
                            return (my_side, reg)
                    for reg in get_edge_regions():
                        if reg not in covered_region:
                            return (my_side, reg)
        if len(moves) >= 6:
            attracks = []
            defence = []
            region_for_2_2 = []
            region_for_2_2_def = []
            for region in get_all_region():
                if region in covered_region:
                    continue
                if my_side == 'O':
                    other_side = 'X'
                else:
                    other_side = 'O'
                win_line = get_win_line(current_broad[my_side],region)
                win_line_oppo = get_win_line(current_broad[other_side],region)
                if win_line:
                    # 连 3
                    attracks.append((my_side,region))
                if win_line_oppo:
                    # 堵住
                    defence.append((my_side,region))
                line2s = get_2_on_line(current_broad[my_side],region,current_broad[other_side])

                if len(line2s)>=2:
                    region_for_2_2.append((my_side,region))
                line2s = get_2_on_line(current_broad[other_side], region, current_broad[my_side])
                if len(line2s) >= 2:
                    region_for_2_2_def.append((my_side, region))

            if len(attracks)>0:
                return attracks[0]
            elif len(defence)>0:
                return defence[0]
            elif len(region_for_2_2)>0:
                return region_for_2_2[0]
            elif len(region_for_2_2_def)>0:
                return region_for_2_2_def[0]
            else:
                if 'C' not in covered_region:
                    return (my_side,"C")
                for reg in  get_corner_regions():
                    if reg not in covered_region:
                        return (my_side,reg)
                for reg in get_edge_regions():
                    if reg not in covered_region:
                        return (my_side, reg)
    elif my_side == 'X':
        first_move = moves[0][1]

        if moves[0][1] == 'C':
            if len(moves)==1:
                return ('X','SE')
            if len(moves) == 3:
                sec_move = moves[2][1]
                if sec_move == 'NW':
                    return ('X','NE')
                else:
                    # lian 2
                    defence = []
                    region_for_2_2 = []
                    region_for_2_2_def = []
                    for region in get_all_region():
                        if region in covered_region:
                            continue
                        win_line_oppo = get_win_line(current_broad['O'], region)

                        if win_line_oppo:
                            # 堵住
                            defence.append(('X', region))
                    if len(defence)>0:
                        return defence[0]
            if len(moves) >= 5:
                my_side = 'X'
                attracks = []
                defence = []
                region_for_2_2 = []
                region_for_2_2_def = []
                for region in get_all_region():
                    if region in covered_region:
                        continue
                    if my_side == 'O':
                        other_side = 'X'
                    else:
                        other_side = 'O'
                    win_line = get_win_line(current_broad[my_side], region)
                    win_line_oppo = get_win_line(current_broad[other_side], region)
                    if win_line:
                        # 连 3
                        attracks.append((my_side, region))
                    if win_line_oppo:
                        # 堵住
                        defence.append((my_side, region))
                    line2s = get_2_on_line(current_broad[my_side], region, current_broad[other_side])
                    if len(line2s) >= 2:
                        region_for_2_2.append((my_side, region))
                    line2s = get_2_on_line(current_broad[other_side], region, current_broad[my_side])
                    if len(line2s) >= 2:
                        region_for_2_2_def.append((my_side, region))

                if len(attracks) > 0:
                    return attracks[0]
                elif len(defence) > 0:
                    return defence[0]
                elif len(region_for_2_2) > 0:
                    return region_for_2_2[0]
                elif len(region_for_2_2_def) > 0:
                    return region_for_2_2_def[0]
                else:
                    if 'C' not in covered_region:
                        return (my_side, "C")
                    for reg in get_corner_regions():
                        if reg not in covered_region:
                            return (my_side, reg)
                    for reg in  get_edge_regions():
                        if reg not in covered_region:
                            return (my_side, reg)
        elif moves[0][1] in get_edge_regions():
            if len(moves)==1:
                return ('X','C')
            elif len(moves) ==3:
                new_move = moves[2][1]

                oppo_map = get_oppo_map()
                if oppo_map.get(moves[0][1])   == moves[2][1] :
                    regs = [u for u in  get_edge_regions() if u not in [moves[0][1],moves[2][1]]]
                    return  ('X',regs[0])
                elif moves[2][1] in  get_edge_regions():
                    # 相邻
                    a = get_N_S(moves[0][1]+ moves[2][1])+get_W_E(moves[0][1]+ moves[2][1])
                    a = ''.join(a)
                    return ('X',a)
                elif new_move in get_corner_regions() and first_move not in new_move:
                    neighs = get_neigh_corner(new_move)
                    neigh = [u for u in neighs if first_move in u][0]
                    return  ('X',neigh)
                elif first_move in new_move:
                    # 相邻
                    neighs = get_neigh_corner(new_move)
                    neigh = [u for u in neighs if first_move in u][0]
                    return ('X', neigh)
            elif len(moves) >=5:
                attracks = []
                defence = []
                region_for_2_2 = []
                region_for_2_2_def = []
                for region in get_all_region():
                    if region in covered_region:
                        continue
                    if my_side == 'O':
                        other_side = 'X'
                    else:
                        other_side = 'O'
                    win_line = get_win_line(current_broad[my_side], region)
                    win_line_oppo = get_win_line(current_broad[other_side], region)
                    if win_line:
                        # 连 3
                        attracks.append((my_side, region))
                    if win_line_oppo:
                        # 堵住
                        defence.append((my_side, region))
                    line2s = get_2_on_line(current_broad[my_side], region, current_broad[other_side])
                    if len(line2s) >= 2:
                        region_for_2_2.append((my_side, region))
                    line2s = get_2_on_line(current_broad[other_side], region, current_broad[my_side])
                    if len(line2s) >= 2:
                        region_for_2_2_def.append((my_side, region))

                if len(attracks) > 0:
                    return attracks[0]
                elif len(defence) > 0:
                    return defence[0]
                elif len(region_for_2_2) > 0:
                    return region_for_2_2[0]
                elif len(region_for_2_2_def) > 0:
                    return region_for_2_2_def[0]
                else:
                    if 'C' not in covered_region:
                        return (my_side, "C")
                    for reg in get_corner_regions():
                        if reg not in covered_region:
                            return (my_side, reg)
                    for reg in  get_edge_regions():
                        if reg not in covered_region:
                            return (my_side, reg)
        elif moves[0][1] in get_corner_regions():# at corner
            first_move = moves[0][1]
            new_move = moves[2][1]
            if len(moves) ==1:
                return (my_side, 'C')
            elif len(moves) ==3:
                if new_move in get_neigh_corner(first_move):
                    edge = get_same_edge(first_move,new_move)
                    return (my_side, edge)
                elif new_move in first_move:
                    # 先角落 后边
                    edge = get_same_edge(first_move, new_move)
                    next_move = [cor for cor in get_corner_regions() if edge in cor and cor != first_move]
                    return (my_side, next_move[0])
                elif new_move in  get_edge_regions() and new_move not in first_move:
                    # 相邻
                    neighs = get_neigh_corner(first_move)
                    neigh = [u for u in neighs if new_move in u][0]
                    return (my_side, neigh)
                elif new_move == get_oppo_corner(first_move):# diagonal
                    # NSEW random
                    return (my_side, 'N')
            elif len(moves) >= 5:
                attracks = []
                defence = []
                region_for_2_2 = []
                region_for_2_2_def = []
                for region in get_all_region():
                    if region in covered_region:
                        continue
                    if my_side == 'O':
                        other_side = 'X'
                    else:
                        other_side = 'O'
                    win_line = get_win_line(current_broad[my_side], region)
                    win_line_oppo = get_win_line(current_broad[other_side], region)
                    if win_line:
                        # 连 3
                        attracks.append((my_side, region))
                    if win_line_oppo:
                        # 堵住
                        defence.append((my_side, region))
                    line2s = get_2_on_line(current_broad[my_side], region, current_broad[other_side])
                    if len(line2s) >= 2:
                        region_for_2_2.append((my_side, region))
                    line2s = get_2_on_line(current_broad[other_side], region, current_broad[my_side])
                    if len(line2s) >= 2:
                        region_for_2_2_def.append((my_side, region))

                if len(attracks) > 0:
                    return attracks[0]
                elif len(defence) > 0:
                    return defence[0]
                elif len(region_for_2_2) > 0:
                    return region_for_2_2[0]
                elif len(region_for_2_2_def) > 0:
                    return region_for_2_2_def[0]
                else:
                    if 'C' not in covered_region:
                        return (my_side, "C")
                    for reg in get_corner_regions():
                        if reg not in covered_region:
                            return (my_side, reg)
                    for reg in  get_edge_regions():
                        if reg not in covered_region:
                            return (my_side, reg)


def list_compare(a,b):
    """
    检测 a是否被包含在b中
    :param a: 
    :param b: 
    :return: 
    """
    for e in a:
        if e not in b:
            return False
    return True

def get_win_line(current_regions,region):
    """
    得到落在region位置的子的 连3 线
    :param current_regions: 已有子
    :param region: 当前子
    :return: 
    """
    lines = get_possible_pattern(region)
    for line in lines:
        possible_line = current_regions + [region]
        if list_compare(line, possible_line):
            return line
    return None

def get_lost_region_from_line2(line2):
    """
    得到缺少的子 的位置
    :param line2: 一条线有2子同色
    :return: 
    """
    lines = win_pattern()
    for line in lines:
        if list_compare(line2,line):
            return [ u for u in line if  u not in line2][0]


def get_2_on_line(current_regions,region,oppo_regions):
    """
    得到当前有2子同色的线，且没有对方的子
    :param current_regions: 
    :param region: 
    :param oppo_regions: 
    :return: 
    """
    line2s = get_possible_2_pattern(region)
    patterns = []
    for line in line2s:
        possible_line = current_regions + [region]
        if list_compare(line, possible_line) :
            lost_region =  get_lost_region_from_line2(line)
            if lost_region not in oppo_regions:
                patterns.append(line)
    return patterns


def get_all_region():
    return ['NW','N','NE']+['W','C','E']+  ['SW','S','SE']



def win_pattern():
    """
    所有3子的线
    :return: 
    """
    ps = [
        ['NW','N','NE'],
        ['W','C','E'],
        ['SW', 'S', 'SE'],
        ['NW', 'W', 'SW'],
        ['N', 'C', 'S'],
        ['NE', 'E', 'SE'],
        ['NW','C','SE'],
        ['SW','C','NE']
    ]
    return ps

def get_possible_pattern(region):
    """
    包含当前region棋子的 3子连线
    :param region: 
    :return: 
    """
    ps = win_pattern()
    return [p for p in ps if region in p]

def get_possible_2_pattern(region):
    """
    得到所有的2子线
    :param region: 
    :return: 
    """
    ps = get_possible_pattern(region)
    news = []
    for pat in ps:
        for i in range(3):
            sub = [e for i_ ,e in enumerate(pat) if i_ != i]
            news.append(sub)
    return news



def sb2corord(sb):
    N = {'x':0,'y':1}
    S = {'x':0,'y':-1}
    W = {'x':-1,'y':0}
    E = {'x':1,'y':0}
    change_d = {
        'N':N,
        'S':S,
        'W':W,
        'E':E
    }
    coord = [0,0]
    x, y = tuple(coord)
    for c in sb:
        x += change_d[c]['x']
        y += change_d[c]['y']
    return (x,y)

# res= sb2corord('NW')
# print(res)
#
# res = sb2corord('NE')
# print(res)
