#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: Shu Jiang
# time  : 2020/3/13
# 大富翁模拟局
# 待加入：CP检测

import random, math

# 棋盘格
border_num = 36

# 玩家
player_nums = 4
play_turns = 50


# 金钱相关
start_money = 15000 # 玩家初始资金
start_bonus = 2000  # 起点奖励

# 地图定义
toll_map = [
0, 2, 13, 1, -1, 9, 6, 14, 4, 10, -2, 
0, 8, 5, 14, -1, 4, 9, 
0, 1, 12, 2, -2, 14, 3, 11, -1, 8, 7, 
0, -2, 6, 5, 14, 7, 3
]
# -2 命运 -1机会 0 角落格 

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
special_fee_list = [2000,1000,3000,6000,10000]
# 各玩家拥有特殊产业的数量
special_num = [0]*player_nums  


# 产业等级 
assets_levels = 4

# 产业等级记录 lv0-lv4
assest_level_list = [-1]*border_num 

# 产业所有权归属 -1无人 -2不可买 0~ 属于对应玩家
assest_ownship_list = [
-2, -1, -1, -1, -2, -1, -1, -1, -1, -1, -2, 
-2, -1, -1, -1, -2, -1, -1, 
-2, -1, -1, -1, -2, -1, -1, -1, -2, -1, -1, 
-2, -2, -1, -1, -1, -1, -1
]

# CP/组合检测
combo_list = [
[1,2,3],[5,6],[8,9],
[12,13],[16,17],
[19,20,21],[24,25],[27,28],
[31,32],[34,35]
]

# CP增益
cp_plus_per = 15
combo_plus_per = 30

'''
检查该格是否是CP/组合，并返回增益百分比
'''
def combo_check(pos, owner):
    # print(assest_ownship_list[pos])
    for combo in  combo_list:
        if pos in combo:
            for p in combo:
                if not assest_ownship_list[p] == owner:
                    return 0
            if len(combo) == 2: return cp_plus_per
            elif len(combo) == 3: return combo_plus_per
    return 0

'''
投掷骰子
'''
def roll_dice():
    roll = random.randint(1, 6)
    return roll


def play_game(player_nums, play_turns, border_num):
    step_sum = []        # 每位玩家的步数和
    roll_record = []     # 每位玩家的投掷记录
    step_record = []     # 每位玩家的步数和记录
    cost_record = []     # 每位玩家的花费记录
    circle_record = []   # 每位玩家的圈数记录
    pos_record = []      # 每位玩家的位置记录
    pos_stat = []        # 棋盘上各点的位置统计
    money_record = []    # 每位玩家的当前资金记录
    money_now = []       # 每位玩家的当前资金
    
    for i in range(player_nums): # 数组初始化
        step_sum.append(0) 
        money_now.append(start_money) 
        roll_record.append([])
        step_record.append([])
        cost_record.append([])
        circle_record.append([])
        pos_record.append([])
        pos_stat.append([0]* border_num)
        money_record.append([])
        
    pre_pos = 0
    for j in range(play_turns):
        for i in range(player_nums):
            
            
            roll = roll_dice()      # 投掷骰子
            # print((i,j,roll))
            step_sum[i] += roll
            roll_record[i].append(roll)
            step_record[i].append(step_sum[i])
            circle = step_sum[i]/border_num
            pos = step_sum[i]%border_num
            if j>0: pre_pos = pos_record[i][-1]
            circle_record[i].append(circle)
            pos_record[i].append(pos)
            pos_stat[i][pos] += 1 # 获取点数存储到对应次数位置
            
            
            # 经过起点 +2000
            if pre_pos > pos :
                print('START: Player %d: go past the start and get bonus $%d.'%(i,start_bonus))
                money_now[i]+=start_bonus  
            
            # 购买土地
            if assest_ownship_list[pos] == -1:
                assets_type = toll_map[pos]
                if assets_type == 14: # 特殊产业
                    special_num[i] += 1
                    cost = special_fee_list[0]
                    print('BUY: Player %d: buy SPECIAL assert at %d and cost $%d; now have %d SPECIAL.'%(i,pos,cost,special_num[i]))
                else:
                    cost = assets_list[assets_type][0]
                    assest_level_list[pos] = 0
                    print('Player %d: buy assert at %d (type %d) and cost $%d.'%(i,pos,assets_type,cost))
                assest_ownship_list[pos] = i
                money_now[i] -= cost
                
            # 升级自己的产业
            elif assest_ownship_list[pos] == i:
                assets_type = toll_map[pos]
                level = assest_level_list[pos]
                if level < assets_levels and assets_type < 14:
                    cost = assets_list[assets_type][1]
                    assest_level_list[pos] += 1
                    money_now[i] -= cost
                    print('UP: Player %d: update assert at %d (type %d) from level %d to level %d and cost $%d.'%(i,pos,assets_type,level,level+1,cost))

            # 走到别人的产业 
            elif assest_ownship_list[pos] > -1:
                assets_type = toll_map[pos]
                owner = assest_ownship_list[pos]
                level = assest_level_list[pos]
                if assets_type == 14: # 特殊产业
                    num = special_num[owner]
                    fee = special_fee_list[num]
                    print('PAY: Player %d: stay at %d (SPECIAL) and pay $%d to Player %d who has %d SPECIAL.'%(i,pos,fee,owner,special_num[owner]))
                else: #正常产业
                    fee = assets_list[assets_type][level+2]
                    fee_plus = math.ceil(1.0*fee*combo_check(pos,owner)/1000)*10
                    if fee_plus>0: 
                        # CP/组合增益
                        print('COMBO: Player %d: stay at %d (type %d, level %d)) and pay $%d ($%d + $%d) to Player %d.'%(i,pos,assets_type,level,fee+fee_plus, fee,fee_plus, owner))
                    else:
                        print('PAY: Player %d: stay at %d (type %d, level %d)) and pay $%d to Player %d.'%(i,pos,assets_type,level,fee,owner))
                    
                money_now[i] -= fee
                money_now[owner] += fee
            
            money_record[i].append(money_now[i])
            
            print('====STATUS====')
            print('Player %d:' % i)
            print('roll %d:' % roll)
            print('circle: %d' % circle)
            print('position: %d' % pos)
            print('money: %d' % money_now[i])
            print('==============')
            
    # print(roll_record)
    # print(step_record)
    # print(circle_record)
    # print(pos_record)
    # print(pos_stat)
    
    print(money_record)
    print(assest_ownship_list)
    print(assest_level_list)
    

    for i in range(player_nums):
        print('============')
        print('Player %d:' % i)
        print('circle: %d' % circle_record[i][-1])
        print('position: %d' % pos_record[i][-1])
        print('money: %d' % money_now[i])
        
        
def border_record(player_nums, border_num):
    ### 有地图保存
    step_sum = []        # 每位玩家的步数和
    roll_record = []     # 每位玩家的投掷记录
    step_record = []     # 每位玩家的步数和记录
    cost_record = []     # 每位玩家的花费记录
    circle_record = []   # 每位玩家的圈数记录
    pos_record = []      # 每位玩家的位置记录
    pos_stat = []        # 棋盘上各点的位置统计
    money_record = []    # 每位玩家的当前资金记录
    money_now = []       # 每位玩家的当前资金
    
    for i in range(player_nums): # 数组初始化
        step_sum.append(0) 
        money_now.append(start_money) 
        roll_record.append([])
        step_record.append([])
        cost_record.append([])
        circle_record.append([])
        pos_record.append([])
        pos_stat.append([0]* border_num)
        money_record.append([])
        
    pre_pos = 0
    for j in range(play_turns):
        print('Turn No. %d:' % j)
        print('============')
        for i in range(player_nums):
            # roll = roll_dice()      # 投掷骰子
            roll = int(raw_input('Player %d roll the dice:'%i))%6 or 6
            # print((i,j,roll))
            step_sum[i] += roll
            roll_record[i].append(roll)
            step_record[i].append(step_sum[i])
            circle = step_sum[i]/border_num
            pos = step_sum[i]%border_num
            if j>0: pre_pos = pos_record[i][-1]
            circle_record[i].append(circle)
            pos_record[i].append(pos)
            pos_stat[i][pos] += 1 # 获取点数存储到对应次数位置

            print('Player %d:' % i)
            print('circle: %d' % circle)
            print('position: %d' % pos)
            print('============')
            



if __name__ == '__main__':
    play_game(player_nums, play_turns, border_num)
    # border_record(player_nums, border_num)
    
    
    


