
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup

import requests

# https://www.bbc.co.uk/sport/football/teams/leeds-united/scores-fixtures
# http_scores_fixtures  = "https://www.bbc.co.uk/sport/football/teams/leeds-united/scores-fixtures" 
# http_scores_fixtures  = "https://www.bbc.co.uk/sport/football/teams/leeds-united/scores-fixtures/2021-01" 
# http_scores_fixtures  = "https://www.bbc.co.uk/sport/football/55769208"

#result  = requests.get(http_scores_fixtures)

#result.status_code

# rcontents = result.content

# stat_soup = BeautifulSoup(rcontents, 'html.parser')

#rawfile='/Users/brianellwood/football_stats/page.dat'
#rf = open(rawfile,'w')
#rf.write (stat_soup.prettify())
#rf.close()

#rawfile2 = open('/Users/brianellwood/football_stats/page.dat', 'r')

#stat_soup2 = BeautifulSoup(rawfile2, 'html.parser')

#rawfile2.close()

#for link in stat_soup2.find_all('a'):
#    alink = link.get('href')
    #print(alink)
#    if '/sport/football/' in alink:
#        if 'team' not in alink:
#            if 'scores' not in alink:
#                print(alink)
                #/sport/football/55769208
#     print(fred)

# for link in stat_soup.find_all('a'):
#     fred = link.get('href')
    # if 'scores-fixtures/2' in fred:
    #  print(fred)
#     print(fred)


# using file instead of url until worked how what to scrape
rawfile3 = open('/Users/brianellwood/football_stats/page_dets.dat', 'r')
# rawfile3 = open('/Users/brianellwood/football_stats/snippet.dat', 'r')

stat_soup3 = BeautifulSoup(rawfile3, 'html.parser')

rawfile3.close()

# stat_soup3.find_all('span',{"sp-c-lineup-pitch__player__name gs-u-display-block@xs"}):  - just starting 11 h/a
# stat_soup3.find_all('span',{"sp-c-lineup-pitch__player"}): - this gives number and player starting 11 h/a
# stat_soup3.find_all('span',{"gel-pica-bold sp-c-team-lineups__number"}): - gives squad numbers
# stat_soup3.find_all('span',{"gs-u-vh"}): - bookinkins subs but not the name or number
# 
# 
home = "-"
away = "-"
ignore_list = ('Average','Half Time','Played','Won','Chelsea', 'Burnley', 'Full Time', 'Leicester City', 'Leeds United', 
'Full Time', 'West Ham United', 'Liverpool', 'Full Time', 'Brighton & Hove Albion', 'Tottenham Hotspur',
'Drawn', 'Lost', 'Goals for', 'Goals against', 'Goal difference', 'Points', 'Manchester City', 'Manchester United', 
'Liverpool', 'Leicester City', 'West Ham United', 'Tottenham Hotspur', 'Chelsea', 'Everton', 'Aston Villa', 'Arsenal', 
'Southampton', 'Leeds United', 'Crystal Palace', 'Wolverhampton Wanderers', 'Newcastle United', 
'Burnley', 'Brighton & Hove Albion', 'Fulham', 'West Bromwich Albion', 'Sheffield United')


# get list of squad numbers
def get_squad_num():
    for link in stat_soup3.find_all('span',{"gel-pica-bold sp-c-team-lineups__number"}):
        link1 = link.text.strip()
        squad_num.append(link1)
    return squad_num

# this gets all playes plus some uneeded stuff no number, players inlist twice so could be used subs
def get_player_list():
    cnt_1 = 1
    for link in stat_soup3.find_all('abbr'):
        if cnt_1 == 1:
            home = link.attrs['title']
        elif cnt_1 == 2:
            away = link.attrs['title']
        elif link.attrs['title'] not in ignore_list:
            player_list.append(link.attrs['title'])
        cnt_1 += 1
    return player_list,home,away

# gets the starting 11 for home and awy
def get_teams():   
    cnt_2 = 1
    for link in stat_soup3.find_all('span',{"sp-c-lineup-pitch__player"}):
        link1 = link.text.strip()
        link1 = link1.replace('\n','')
        squad_no = link1.split(" ")[0]
        player = link1.split(" ")[-1]
        squad_player = (squad_no +';'+ player)
        if cnt_2 <= 11:
            home_team.append(squad_player)
        else:
            away_team.append(squad_player)
        cnt_2 +=1
    return home_team, away_team

# gets a the lists of hame and away players and used subs..needs ammending to use home_squad_no      
def get_player_sub():
    cnt_3 = 0
    hcnt_4 = 0
    hcnt_player_list = 0
    acnt_4 = 0
    acnt_player_list = 0
    for strt_player in player_list:
        if home_team[0].split(";")[1] in  player_list[cnt_3]:
            hcnt_player_list = cnt_3
            while hcnt_4 < 11:
                if home_team[hcnt_4].split(";")[1] in  player_list[hcnt_player_list]:
                    pl_sub = home_team[hcnt_4]+" ; - "
                    hplayer_sub.append(pl_sub)
                    hcnt_4 +=1
                    hcnt_player_list +=1   
                # what if 11th player subbed ?    
                if hcnt_4 <11 and home_team[hcnt_4].split(";")[1] not in  player_list[hcnt_player_list]:  
                    prev_cnt = (hcnt_4 - 1)
                    new_dets = home_team[prev_cnt]+" ; | "+player_list[hcnt_player_list]
                    hplayer_sub[prev_cnt] = new_dets
                    hcnt_player_list +=1
        if away_team[0].split(";")[1] in  player_list[cnt_3]:
            acnt_player_list = cnt_3
            while acnt_4 < 11:
                if away_team[acnt_4].split(";")[1] in  player_list[acnt_player_list]:
                    pl_sub = away_team[acnt_4]+" ; - "
                    aplayer_sub.append(pl_sub)
                    acnt_4 +=1
                    acnt_player_list +=1   
                # what if 11th player subbed ?    
                if acnt_4 < 11 and away_team[acnt_4].split(";")[1] not in  player_list[acnt_player_list]:  
                    prev_cnt = (acnt_4 - 1)
                    new_dets = away_team[prev_cnt]+" ; | "+player_list[acnt_player_list]
                    aplayer_sub[prev_cnt] = new_dets
                    acnt_player_list +=1                
        cnt_3 +=1
    return hplayer_sub, aplayer_sub

#  gets the score for home and away
def get_score():
    for home_score in stat_soup3.find('span',{"sp-c-fixture__number sp-c-fixture__number--home sp-c-fixture__number--ft"}):
        home_score = home_score.replace('\n','')
        home_score = home_score.replace(' ','')

    for away_score in stat_soup3.find('span',{"sp-c-fixture__number sp-c-fixture__number--away sp-c-fixture__number--ft"}):
        away_score = away_score.replace('\n','')
        away_score = away_score.replace(' ','')

    return home_score,away_score 

def get_home_squad():
    ply_cnt = len(player_list)
    cnt_4 = 0
    while cnt_4 < ply_cnt:
        if home_team[0].split(";")[1] in  player_list[cnt_4]:
            cnt_5 = 0
            cnt_6 = 0
            while away_team[0].split(";")[1] not in  player_list[cnt_4]:
                if cnt_5 >= 11:
                    splayer = (player_list[cnt_4].split(" ")[-1])+" ; "
                    home_squad.append(splayer)
                if cnt_5 < 11:
                    if home_team[cnt_5].split(";")[1] in  player_list[cnt_4]:
                        splayer = (player_list[cnt_4].split(" ")[-1])+" ; "
                        home_squad.append(splayer)
                        cnt_5 +=1
                cnt_6 +=1
                cnt_4 +=1 
        cnt_4 +=1
    return home_squad

def get_home_squad_no():
    cnt_7 = 0
    for hplayer in home_squad:
        hplayer_sq = squad_num[cnt_7]+" ; "+home_squad[cnt_7]
        home_squad_no.append(hplayer_sq)
        cnt_7 +=1
    #print('home_squad_no---------------------------------')
    #print(home_squad_no)
    return home_squad_no

def get_subd_squad():
    cnt_8 = 0
    for ply1 in hplayer_sub:
        if '|' in hplayer_sub[cnt_8]:
            hplayer_sub2 = hplayer_sub[cnt_8].split("|")[1]
            indices = [i for i, s in enumerate(home_squad_no) if hplayer_sub2.split(" ")[2] in s]
            subd = hplayer_sub[cnt_8].split("|")[0]
            sub = home_squad_no[indices[0]]
            hplayer_sub[cnt_8] = subd+"| "+sub     
        cnt_8 +=1  
    return ()

def get_fixture_date():
    for gdate in stat_soup3.find_all('time',{"sp-c-fixture__date gel-minion"}):
        fix_date = gdate.text.strip()
    return fix_date

#=======================
squad_num = []
squad_num = get_squad_num()

player_list = []
player_list, home, away = get_player_list()

home_team = []
away_team = []

home_team, away_team = get_teams()

hplayer_sub = []
aplayer_sub = []
hplayer_sub,aplayer_sub = get_player_sub()

fix_date1 = get_fixture_date()

home_score, away_score = get_score()
print('---------------------------------score')
print(fix_date1)
print(home,home_score,away,away_score)
print('---------------------------------score')

home_squad = []
home_squad = get_home_squad()
#print('home_squad---------------------------------')
#print(home_squad)  

home_squad_no = [] 
home_squad_no = get_home_squad_no()
#print('home_squad_no---------------------------------')
#print(home_squad_no)

get_subd_squad()
print('Home team---------------------------------')
print(hplayer_sub)
#=======================




#<span class="sp-c-fixture__number sp-c-fixture__number--home sp-c-fixture__number--ft" data-reactid=".1k16cwn7e.0.0.1.0.0.1.0">
#<span class="sp-c-fixture__number sp-c-fixture__number--away sp-c-fixture__number--ft" data-reactid=".1k16cwn7e.0.0.1.0.2.1.0">







