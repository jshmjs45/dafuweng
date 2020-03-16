#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: Shu Jiang
# time  : 2020/3/13
# 大富翁模拟局
# 已加入：互动设置
# 待加入：卡片抽取

import random, math

# 棋盘格
border_num = 36

# 玩家
player_nums = 0
round_nums = 50


destiny_card_num = 27
chance_card_num = 27

# 金钱相关
start_money = 15000 # 玩家初始资金
start_bonus = 2000  # 起点奖励


# 卡片定义 ID: 0-26
destiny_card_list = range(destiny_card_num)
chance_card_list  = range(chance_card_num)
# 机会卡持有情况 [0-player_nums]: 玩家已抽卡片  [4]: 还可以抽取的卡片
chance_card_ownship = []
# 卡片记录
destiny_card_record = []
chance_card_record = []



# 地图定义 -2 命运 -1机会 0 角落格 
toll_map = [
0, 2, 13, 1, -1, 9, 6, 14, 4, 10, -2, 
0, 8, 5, 14, -1, 4, 9, 
0, 1, 12, 2, -2, 14, 3, 11, -1, 8, 7, 
0, -2, 6, 5, 14, 7, 3
]


# 1-13 正常产业格 [购置费,升级费,lv0,lv1,lv2,lv3,lv4]
assets_list = [
[0,0,0,0,0,0,0],
[600,500,20,100,300,900,2500],
[1000,500,60,300,900,2700,5500],
[1200,500,80,400,1000,3000,6000],
[1400,1000,100,500,1500,4500,7500],
[1600,1000,120,600,1800,5000,9000],
[1800,1000,140,700,2000,5500,9500],
[2000,1000,160,800,2200,6000,10000],
[2200,1500,180,900,2500,7000,10500],
[2600,1500,220,1100,3300,8000,11500],
[2800,1500,240,1200,3600,8500,12000],
[3000,2000,260,1300,3900,9000,12750],
[3200,2000,280,1500,4500,10000,14000],
[4000,2000,500,2000,6000,14000,20000],
]



# 14 特殊产业格 [购置费,x1,x2,x3,x4]
SPECIAL = 14
special_fee_list = [2000,1000,3000,6000,10000]
# 各玩家拥有特殊产业的数量
special_num = [] 


# 产业等级 
assets_levels = 4

# 产业等级记录 lv0-lv4
assest_level_list = [0]*border_num 

# 产业所有权归属 -1无人 -2不可买 0~ 属于对应玩家
assest_owner_list = [
-2, -1, -1, -1, -2, -1, -1, -1, -1, -1, -2, 
-2, -1, -1, -1, -2, -1, -1, 
-2, -1, -1, -1, -2, -1, -1, -1, -2, -1, -1, 
-2, -2, -1, -1, -1, -1, -1
]

# 玩家姓名定义
owner_name_list = []


roll_record = []        # 每位玩家的投掷记录
step_sum = []           # 每位玩家的步数和
circle_record = []      # 每位玩家的圈数记录
pos_record = []         # 每位玩家的位置记录
money_record = []       # 每位玩家的余额记录
money_now = []          # 每位玩家的当前余额
status_record = []      # 每位玩家的状态记录

# CP/组合
combo_list = [
[1,2,3],[5,6],[8,9],
[12,13],[16,17],
[19,20,21],[24,25],[27,28],
[31,32],[34,35]
]

# CP/组合
cp_plus_per = 15
combo_plus_per = 30

'''
添加玩家信息
'''
def add_player_name(player_nums,name):
    owner_name_list.append(name)
    if owner_name_list[player_nums] == name:
        print('ADD SUCESS: The name of Player %d is %s.'%(player_nums,name))
    else:
        print('ADD FAILURE!')
    player_nums+=1    
    return player_nums
    

'''
显示棋盘
'''
def show_border_info():
    print('''


    ''')

'''
显示玩家信息
'''
def show_player_info():
    for i in range(player_nums):
        print('---- PLAYER %d ----' % i)
        print('name: %s' % owner_name_list[i])
        # if not len(roll_record) == 0:
            # if not len(roll_record[i]) == 0:
                # print('roll: %d ' % roll_record[i][-1])
            # else:
                # print('circle: %d ' % 0)
        if not len(circle_record) == 0:
            if not len(circle_record[i]) == 0:
                print('circle: %d ' % circle_record[i][-1])
            else:
                print('circle: %d ' % 0)
        if not len(pos_record) == 0:
            if not len(pos_record[i]) == 0:
                print('position: %d ' % pos_record[i][-1])
            else:
                print('position: %d ' % 0)
        if not len(money_now) == 0:
            print('money: %d ' % money_now[i])
            
        show_assert(i)
        print('------------------')

'''
投掷骰子
'''
def roll_dice():
    roll = random.randint(1, 6)
    return roll

'''
游戏初始化
'''
def game_init(player_nums):
    print('Player number: %d' % player_nums)
    print('GAME initializing...')
    
    for i in range(player_nums): # 数组初始化
        special_num.append(0) 
        step_sum.append(0) 
        roll_record.append([])
        circle_record.append([])
        pos_record.append([])
        money_record.append([])
        money_now.append(start_money) 
        status_record.append([])
        chance_card_ownship.append([])
    
    owner_name_list.append('None') 
    chance_card_ownship.append(chance_card_list) 

'''
显示玩家名下资产
'''
def show_assert(player):
    assest_list = []
    for i in range(border_num):
        type = toll_map[i]
        owner = assest_owner_list[i]
        level = assest_level_list[i]
        if owner == player:
            assest_list.append((i,type,level))
    
    line = 'assest_list (index, type, level): \n'
    for assest in assest_list:
        line += '(%d, %d, %d) ' % assest
        
            
    print(line)
    return assest_list


'''
检查该格是否是CP/组合，并返回增益百分比
'''
def combo_check(pos, owner):
    # print(assest_owner_list[pos])
    for combo in  combo_list:
        if pos in combo:
            for p in combo:
                if not assest_owner_list[p] == owner:
                    return 0
            if len(combo) == 2: return cp_plus_per
            elif len(combo) == 3: return combo_plus_per
    return 0


'''
自动化玩游戏
'''
def play_game(player_nums, round_nums, border_num):

    pre_pos = 0 # 记录上一轮的位置
    for j in range(round_nums):
        for i in range(player_nums):
            roll = roll_dice()      # 投掷骰子
            # print((i,j,roll))
            step_sum[i] += roll
            roll_record[i].append(roll)
            circle = step_sum[i]/border_num
            pos = step_sum[i]%border_num
            if j>0: pre_pos = pos_record[i][-1]
            circle_record[i].append(circle)
            pos_record[i].append(pos)
            
            # 经过起点 +2000
            if pre_pos > pos :
                print('%d: START BONUS: Player %d: go past the start and get bonus $%d.'%(j,i,start_bonus))
                money_now[i]+=start_bonus  
            
            # 购买土地
            if assest_owner_list[pos] == -1:
                assets_type = toll_map[pos]
                # 特殊产业
                if assets_type == SPECIAL: 
                    cost = special_fee_list[0]
                    if money_now[i] > cost:
                        special_num[i] += 1             # 特殊产业数目+1
                        assest_owner_list[pos] = i    # 产业归属设置
                        money_now[i] -= cost            # 扣除花费
                        print('%d: BUY SUCCESS: Player %d: buy SPECIAL assert at %d and cost $%d; now have %d SPECIAL.'%(j,i,pos,cost,special_num[i]))
                    else: # 余额不足
                        print('%d: BUY FAILURE: Player %d: cannot buy SPECIAL assert at %d (cost $%d, money $%d).'%(j,i,pos,cost,money_now[i]))
                
                # 正常产业
                elif assets_type >0 and assets_type < SPECIAL:
                    cost = assets_list[assets_type][0]
                    if money_now[i] > cost:
                        assest_level_list[pos] = 0      # 产业等级置0
                        assest_owner_list[pos] = i    # 产业归属设置
                        money_now[i] -= cost            # 扣除花费
                        print('%d: BUY SUCCESS: Player %d: buy assert at %d (type %d) and cost $%d.'%(j,i,pos,assets_type,cost))
                    else: # 余额不足
                        print('%d: BUY FAILURE: Player %d: cannot buy assert at %d (type %d, cost $%d, money $%d).'%(j,i,pos,assets_type,cost,money_now[i]))
                
                
            # 升级自己的产业
            elif assest_owner_list[pos] == i:
                assets_type = toll_map[pos]
                level = assest_level_list[pos]
                if level < assets_levels and assets_type < SPECIAL:
                    cost = assets_list[assets_type][1]
                    if money_now[i] > cost:
                        assest_level_list[pos] += 1     # 产业等级+1
                        money_now[i] -= cost            # 扣除花费
                        print('%d: UP SUCCESS:  Player %d: upgrade assert at %d (type %d) from level %d to level %d and cost $%d.'%(j,i,pos,assets_type,level,level+1,cost))
                    else: # 余额不足
                        print('%d: UP FAILURE:  Player %d: cannot upgrade assert at %d (type %d, cost $%d, money $%d) from level %d to level %d.'%(j,i,pos,assets_type,cost,money_now[i],level,level+1))


            # 走到别人的产业 
            elif assest_owner_list[pos] > -1:
                assets_type = toll_map[pos]
                owner = assest_owner_list[pos]
                level = assest_level_list[pos]
                if assets_type == SPECIAL: # 特殊产业
                    num = special_num[owner]
                    fee = special_fee_list[num]
                    print('%d: PAY SPECIAL: Player %d: stay at %d (SPECIAL) and pay $%d to Player %d who has %d SPECIAL.'%(j,i,pos,fee,owner,special_num[owner]))
                else: #正常产业
                    fee = assets_list[assets_type][level+2]
                    fee_plus = math.ceil(1.0*fee*combo_check(pos,owner)/1000)*10
                    if fee_plus>0: 
                        # CP/组合增益
                        print('%d: PAY COMBO:   Player %d: stay at %d (type %d, level %d)) and pay $%d ($%d + $%d) to Player %d.'%(j,i,pos,assets_type,level,fee+fee_plus,fee,fee_plus, owner))
                    else:
                        print('%d: PAY SINGLE:  Player %d: stay at %d (type %d, level %d)) and pay $%d to Player %d.'%(j,i,pos,assets_type,level,fee,owner))
                    
                money_now[i] -= fee
                money_now[owner] += fee
            
            money_record[i].append(money_now[i])
            status_record[i].append([i,roll,circle,pos,money_now[i]])
            # print('====STATUS====')
            # print('Player %d:' % i)
            # print('roll %d:' % roll)
            # print('circle: %d' % circle)
            # print('position: %d' % pos)
            # print('money: %d' % money_now[i])
            # print('==============')
    
    for i in range(player_nums):
        print('============')
        print('Player %d:' % i)
        print('circle: %d' % circle_record[i][-1])
        print('position: %d' % pos_record[i][-1])
        print('money: %d' % money_now[i])
    
    
    record_writer('status_record.csv', status_record)
    # record_writer('money_record.csv', money_record)
    # record_writer('position_record.csv', pos_record)
    
    # print(roll_record)
    # print(step_record)
    # print(circle_record)
    # print(pos_record)
    # print(money_record)
    # print(status_record)
    # print(assest_owner_list)
    # print(assest_level_list)
    


   
def record_writer(file, record):
    writer = open(file,'w')
    for j in range(round_nums):
        line = '%d,'%(j)
        for i in range(player_nums):
            for item in record[i][j]:
                line += (str(item) +',')
        # print(line)
        writer.write(line+'\n')    

   
        
def border_record(player_nums, border_num):

    pre_pos = 0 # 记录上一轮的位置
    print('''
    ==== GAME START ====
    ''')
    for j in range(round_nums):
        print('========== ROUND %d ==========' % j)
        for i in range(player_nums):
            print('---------- PLAYER %d ----------' % i)
            # roll = roll_dice()      # 投掷骰子
            
            while(1):
                print('Player %d roll the dice: ' % i)
                input = raw_input()
                if input in ['1','2','3','4','5','6']:
                    roll = int(input)
                    break
                elif input == '':
                    roll = roll_dice()      # 投掷骰子
                    break
                elif input == 'exit':
                    return
                else:
                    print('==== WARNING ====')
                    print('Do you mean to input the following instructions:')
                    print('"exit": exit the game')
            
            step_sum[i] += roll
            roll_record[i].append(roll)
            circle = step_sum[i]/border_num
            pos = step_sum[i]%border_num
            if j>0: pre_pos = pos_record[i][-1]
            circle_record[i].append(circle)
            pos_record[i].append(pos)
            
            print('name: %s  ' % owner_name_list[i])
            print('roll: %d  ' % roll)
            print('money: %d  ' % roll)
            print('circle: %d ' % circle)
            print('position: %d (from %d)' % (pos,pre_pos))
            print('money: $%d ' % money_now[i])
            
            assets_type = toll_map[pos]             #产业类型
            owner = assest_owner_list[pos]   #产业归属
            level = assest_level_list[pos]   #产业等级
            
            # 经过起点 +2000
            if pre_pos > pos :
                print('START BONUS: Player %d: go past the start and get bonus $%d.'%(i,start_bonus))
                money_now[i]+=start_bonus  

            # 特殊产业 14
            if assets_type == SPECIAL: 
                print('+--------POSITION-------+')
                print('|index: %d \t\t|' % pos)
                print('|type: %s \t\t|' % 'SPECIAL')
                print('|owner: %s \t\t|' % owner_name_list[owner])
                
                if owner == -1:      # 无归属 购买土地 
                    cost = special_fee_list[0]
                    print('|cost: $%d \t\t|' % cost)
                    print('+-----------------------+')
                    print('Do you want to BUY it? (Y/n)')
                    input = raw_input()
                    if not input == 'n':
                        if money_now[i] > cost:
                            special_num[i] += 1             # 特殊产业数目+1
                            assest_owner_list[pos] = i      # 产业归属设置
                            money_now[i] -= cost            # 扣除花费
                            print('BUY SUCCESS!')
                        else: # 余额不足
                            print('BUY FAILURE: no enough money!')
                
                elif owner == i:    # 自己的产业
                    print('+-----------------------+')
                
                else: # 别人的产业 付钱
                    num = special_num[owner]
                    fee = special_fee_list[num]

                    print('|num: %d \t\t|' % (num))
                    print('|fee: $%d     \t|' % fee)
                    print('+-----------------------+')
                    print('PAY SPECIAL: Player %d: stay at %d (SPECIAL) and pay $%d to Player %d who has %d SPECIAL.'%(i,pos,fee,owner,num))
                    print('Player %d: $%d (%d - %d)' % (i,     money_now[i]-fee,     money_now[i],     fee))
                    print('Player %d: $%d (%d + %d)' % (owner, money_now[owner]+fee, money_now[owner], fee))
                    money_now[i] -= fee
                    money_now[owner] += fee
            
            # 正常产业 1-13 
            elif assets_type >0 and assets_type < SPECIAL:
                print('+--------POSITION-------+')
                print('|index: %d \t\t|' % pos)
                print('|type: %d  \t\t|' % assets_type)
                print('|owner: %s \t\t|' % owner_name_list[owner])
                print('|level: %d \t\t|' % level)
                
                if   owner == -1:   # 无归属 购买土地 
                    cost = assets_list[assets_type][0]
                    print('|cost: $%d     \t|' % cost)
                    print('+-----------------------+')
                    print('Do you want to BUY it? (Y/n)')
                    input = raw_input()
                    if not input == 'n':
                        if money_now[i] > cost:
                            assest_level_list[pos] = 0      # 产业等级置0
                            assest_owner_list[pos] = i    # 产业归属设置
                            money_now[i] -= cost            # 扣除花费
                            print('BUY SUCCESS')
                            print('balance: $%d ' % (money_now[i]))
                        else: # 余额不足
                            print('BUY FAILURE: no enough money!')

                elif owner == i:    # 升级自己的产业
                    cost = assets_list[assets_type][1]
                    print('|upcost: $%d   \t|' % cost)
                    print('+-----------------------+')
                    print('Do you want to UPGRADE it? (Y/n)')
                    input = raw_input()
                    if not input == 'n':
                        if money_now[i] > cost:
                            assest_level_list[pos] += 1     # 产业等级+1
                            money_now[i] -= cost            # 扣除花费
                            print('UP SUCCESS: upgrade assert at %d (type %d) from level %d to level %d and cost $%d.'%(pos,assets_type,level,level+1,cost))
                            print('balance: $%d ' % (money_now[i]))
                        else: # 余额不足
                            print('UP FAILURE: no enough money!')

                else:    # 别人的产业 付钱
                    fee = assets_list[assets_type][level+2]
                    fee_plus = math.ceil(1.0*fee*combo_check(pos,owner)/1000)*10
                    
                    print('|fee: $%d (+$%d)   \t|' % (fee,fee_plus))
                    print('+-----------------------+')
                    if fee_plus>0: 
                        # CP/组合增益
                        print('PAY COMBO: Player %d: stay at %d (type %d, level %d)) and pay $%d ($%d + $%d) to Player %d.'%(i,pos,assets_type,level,fee+fee_plus,fee,fee_plus, owner))
                    else:
                        print('PAY SINGLE: Player %d: stay at %d (type %d, level %d) and pay $%d to Player %d.'%(i,pos,assets_type,level,fee,owner))
                    
                    
                    fee += fee_plus
                    print('Player %d: $%d (%d - %d)' % (i,     money_now[i]-fee,     money_now[i],     fee))
                    print('Player %d: $%d (%d + %d)' % (owner, money_now[owner]+fee, money_now[owner], fee))
                    money_now[i] -= fee
                    money_now[owner] += fee

            # 角落格 0
            elif assets_type == 0:
                print('======== CORNER ==========')
            
            # 机会格 -1 
            elif assets_type == -1:
                print('====== CHANCE TIME =======')

            # 命运格 -2 
            elif assets_type == -2:
                print('====== DESTINY TIME ======')
            
            
            money_record[i].append(money_now[i])
            status_record[i].append([i,roll,circle,pos,money_now[i]])
            
            # show_assert(i)

            # print('---- STATUS -----')
            # print('Player: %d ' % i)
            # print('roll: %d  ' % roll)
            # print('circle: %d ' % circle)
            # print('position: %d ' % pos)
            
            print('------------------------------')
            
    show_player_info()
            



if __name__ == '__main__':
    while(1):
        print(u'''
        +------------------+
        |    杨村大富翁    |
        +------------------+
        | 1. 添加玩家      |
        | 2. 显示现有玩家  |
        | 3. 开始游戏      |
        | 4. 开始自动游戏  |
        | 5. 退出游戏      |
        +------------------+
        ''')

        input = raw_input('Please input the number:')
        
        if input == '1':
            print('Please input the name of Player %d:'%player_nums)
            input = raw_input()
            print(player_nums)
            player_nums = add_player_name(player_nums, input)

        if input == '2':
            show_player_info()
        
        if input == '3':
            if player_nums==0: 
                player_nums = 4
                owner_name_list = ['a','b','c','d']
                
            game_init(player_nums)
            border_record(player_nums, border_num)
            exit()
        if input == '4':
            if player_nums==0: 
                player_nums = 4
                owner_name_list = ['a','b','c','d']
            
            game_init(player_nums)
            play_game(player_nums, round_nums, border_num)
            exit()
        
        if input == '5':
            exit()
    
    


