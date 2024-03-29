
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup

import requests

import os.path

####
# get the leeds scores and fixtures pages
####

# https://www.bbc.co.uk/sport/football/teams/leeds-united/scores-fixtures
http_scores_fixtures  = "https://www.bbc.co.uk/sport/football/teams/leeds-united/scores-fixtures" 
# http_scores_fixtures  = "https://www.bbc.co.uk/sport/football/teams/leeds-united/scores-fixtures/2021-01" 
# http_scores_fixtures  = "https://www.bbc.co.uk/sport/football/55769208"

result  = requests.get(http_scores_fixtures)
rcontents = result.content

stat_soup = BeautifulSoup(rcontents, 'html.parser')

#rawfile='/Users/brianellwood/football_stats/page.dat'
#rf = open(rawfile,'w')
#rf.write (stat_soup.prettify())
#rf.close()

#rawfile2 = open('/Users/brianellwood/football_stats/page.dat', 'r')

#stat_soup2 = BeautifulSoup(rawfile2, 'html.parser')
#rawfile2.close()

# this section finds all the leeds month fixture/result pages and writes to a file


#print("start")
# checks for the list of fixtures if not there populates it
if os.path.isfile('/Users/brianellwood/football_stats/fixtures_month.txt') != True:
    print('bugger')
    fixture_month = open('/Users/brianellwood/football_stats/fixtures_month.txt', 'w')

    for link in stat_soup.find_all('a'):
        alink = link.get('href')

        if 'leeds-united/scores-fixtures/20' in alink:
            fixture_month.write(alink+ '\n')
    fixture_month.close()


# takes the fixture_month and get each game url for that month
fixture_month_check = open('/Users/brianellwood/football_stats/fixtures_month.txt', 'r')
fixture_number = open('/Users/brianellwood/football_stats/fixtures_number.txt', 'w')
for line in fixture_month_check:
    line = line.replace("\n", "")
    if '/sport/football/teams/leeds-united/scores-fixtures/2021-03' in line: # just to limit while in dev
        line = 'https://www.bbc.co.uk'+line
        #print('line-------')
        #print(line)
        result_month  = requests.get(line)
        rm_contents = result_month.content
        result_month_soup = BeautifulSoup(rm_contents, 'html.parser')
        for link in result_month_soup.find_all('a'):
            alink = link.get('href')
            if '/sport/football/' in alink and '/sport/football/teams' not in alink and '/sport/football/scores' not in alink:
                alink = 'https://www.bbc.co.uk'+alink
                fixture_number.write(alink+ '\n')
                print(alink)
        fixture_number.close()

#https://www.bbc.co.uk/sport/football/premier-league/scores-fixtures/2021-03

# not sure why doing it like this, what happens if not there
def get_fixture():
    if os.path.isfile('/Users/brianellwood/football_stats/fixtures_number.txt') == True:
        fixture_number = open('/Users/brianellwood/football_stats/fixtures_number.txt', 'r')
        for line in fixture_number:
            fixture = line
        fixture_number.close()
    return(fixture)

#fred=get_fixture()
fred='https://www.bbc.co.uk/sport/football/56369110'
print("Fixture >>>>>")
print(fred)

#/sport/football/teams/leeds-united/scores-fixtures/2022-03

# obvs been on the glue at this point. checks if ive created a file of the html and if not creates one 
# though only needed while testing 
if os.path.isfile('/Users/brianellwood/football_stats/page21.dat') == True:
    rawfile3 = open('/Users/brianellwood/football_stats/page21.dat', 'r')
else:
    result2  = requests.get(fred)
    if result2.status_code == 200:
        rcontents2 = result2.content
        stat_soup3 = BeautifulSoup(rcontents2, 'html.parser')
        rawfile3='/Users/brianellwood/football_stats/page21.dat'
        rf = open(rawfile3,'w')
        rf.write (stat_soup3.prettify())
        rf.close()
        rawfile3 = open('/Users/brianellwood/football_stats/page21.dat', 'r')
    else:
        print("status code",result2.status_code)
        Print()



# using file instead of url until worked how what to scrape
#  comment out while using stat3 above ## 
## rawfile3 = open('/Users/brianellwood/football_stats/page_dets.dat', 'r')
# rawfile3 = open('/Users/brianellwood/football_stats/snippet.dat', 'r')

stat_soup3 = BeautifulSoup(rawfile3, 'html.parser')

rawfile3.close()

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
    #print(home_team)
    #print("<---------------------------->")
    #print(player_list)
    for strt_player in player_list:
        if home_team[0].split(";")[1] in  player_list[cnt_3]:
            hcnt_player_list = cnt_3#+1 ### so goal keeper was man of match so appeared twice at begining og list is mom always first ?
            while hcnt_4 < 11:
                if home_team[hcnt_4].split(";")[1] in  player_list[hcnt_player_list]:
                    if home_team[hcnt_4].split(";")[1] in homescorer:
                        goals = ",1"
                    else:
                        goals = ",0"
                    pl_sub = home_team[hcnt_4]+" "+goals+" ; - "
                    hplayer_sub.append(pl_sub)
                    hcnt_4 +=1
                    hcnt_player_list +=1   
                    print(pl_sub)
                # what if 11th player subbed ?    
                else:
                    prev_cnt = (hcnt_4 - 1)
                    #print("home_team>>>>>>",home_team[hcnt_4].split(";")[1]) 
                    #print("player list----",player_list[hcnt_player_list])
                    new_dets = home_team[prev_cnt]+" ; | "+player_list[hcnt_player_list]
                    hplayer_sub[prev_cnt] = new_dets
                    hcnt_player_list +=1
        if away_team[0].split(";")[1] in  player_list[cnt_3]:
            acnt_player_list = cnt_3
            while acnt_4 < 11:
                if away_team[acnt_4].split(";")[1] in  player_list[acnt_player_list]:
                    if away_team[acnt_4].split(";")[1] in awayscorer:
                        goals = ",1"
                    else:
                        goals = ",0"
                    pl_sub = away_team[acnt_4]+" "+goals+" ; - " # this must be it
                    aplayer_sub.append(pl_sub)
                    acnt_4 +=1
                    acnt_player_list +=1   
                    #print(pl_sub)
                # what if 11th player subbed ?    
                if acnt_4 < 11 and away_team[acnt_4].split(";")[1] not in  player_list[acnt_player_list]: 
                    prev_cnt = (acnt_4 - 1)
                    if player_list[acnt_player_list].split(" ")[1] in awayscorer:
                        goals = ",1"
                    else:
                        goals = ",0"
                    new_dets = pl_sub+" ; | "+player_list[acnt_player_list]+" "+goals
                    new_dets = new_dets.replace("; -","")
                    aplayer_sub[prev_cnt] = new_dets
                    acnt_player_list +=1                
        cnt_3 +=1
    #print(aplayer_sub)
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

def get_away_squad():
    ply_cnt = len(player_list)
    cnt_4 = 0
    while cnt_4 < ply_cnt:
        if away_team[0].split(";")[1] in  player_list[cnt_4]:
            cnt_5 = 0
            cnt_6 = 0
            cnt_7 = cnt_4
            while cnt_7 < ply_cnt:
                if cnt_5 >= 11:
                    splayer = (player_list[cnt_4].split(" ")[-1])+" ; "
                    away_squad.append(splayer)
                if cnt_5 < 11:
                    if away_team[cnt_5].split(";")[1] in  player_list[cnt_4]:
                        splayer = (player_list[cnt_4].split(" ")[-1])+" ; "
                        away_squad.append(splayer)
                        cnt_5 +=1
                cnt_6 +=1
                cnt_4 +=1 
                cnt_7 +=1
        cnt_4 +=1
    return away_squad

def get_home_squad_no():
    cnt_7 = 0
    for hplayer in home_squad:
        goals = "0"
        hplayer_sq = squad_num[cnt_7]+" ; "+home_squad[cnt_7]+" "+goals
        home_squad_no.append(hplayer_sq)
        #print(cnt_7," ^ ",hplayer_sq)
        cnt_7 +=1
    #print('home_squad_no---------------------------------')
    #print(home_squad_no)
    #print(cnt_7)
    return home_squad_no,cnt_7

def get_away_squad_no(sqd_cnt):
    cnt_7 = sqd_cnt
    cnt_8 = 0
    #print("------------------------------------------8.1")
    for aplayer in away_squad:
        goals = "0" # work on seting goal scores 
        #print("squad_num---",squad_num)
        aplayer_sq = squad_num[cnt_7]+" ; "+away_squad[cnt_8]+" "+goals
        #print(">>>")
        #print(cnt_7,cnt_8," ^ ",aplayer_sq)
        away_squad_no.append(aplayer_sq)
        cnt_7 +=1
        cnt_8 +=1
    #print('away_squad_no---------------------------------')
    #print(away_squad_no)
    return away_squad_no

def get_subd_hsquad():
    cnt_8 = 0
    for ply1 in hplayer_sub:
        if '|' in hplayer_sub[cnt_8]:
            hplayer_sub2 = hplayer_sub[cnt_8].split("|")[1]
            indices = [i for i, s in enumerate(home_squad_no) if hplayer_sub2.split(" ")[2] in s]
            subd = hplayer_sub[cnt_8].split("|")[0]
            sub = home_squad_no[indices[0]]
            hplayer_sub[cnt_8] = subd.replace(" ","")+"|,"+sub.replace(" ","")+",0,-,0"     
        cnt_8 +=1  
    return ()

def get_subd_asquad():
    cnt_8 = 0
    for ply1 in aplayer_sub:
        if '|' in aplayer_sub[cnt_8]:
            aplayer_sub2 = aplayer_sub[cnt_8].split("|")[1]
            indices = [i for i, s in enumerate(away_squad_no) if aplayer_sub2.split(" ")[2] in s]
            subd = aplayer_sub[cnt_8].split("|")[0]
            sub = away_squad_no[indices[0]]
            aplayer_sub[cnt_8] = subd.replace(" ","")+"|,"+sub.replace(" ","")+",0,-,0"  
        cnt_8 +=1  
    return ()

def get_fixture_date():
    for gdate in stat_soup3.find_all('time',{"sp-c-fixture__date gel-minion"}):
        fix_date = gdate.text.strip()
    return fix_date

def get_away_scorers():
    scrs = ""
    for aw_scr in stat_soup3.find_all('ul',{"sp-c-fixture__scorers-away"}):
        all_aw_scr = ""
        for aw_scr1 in aw_scr.find_all('span'):
            #aw_scr1 = aw_scr.find('span')
            aw_scr2 = aw_scr1.text.strip()
            aw_scr2 = aw_scr2.replace('\n','')
            aw_scr2 = aw_scr2.replace(' ','')
            all_aw_scr = all_aw_scr+aw_scr2
            #print(all_aw_scr)
            #print("---")
    count = all_aw_scr.count(",")
    #print(count)
    cnt_scrs = count+1
    #print(cnt_scrs)
    cnt = 1
    #score = ""
    while cnt <= cnt_scrs:
        score = all_aw_scr.split(",")[cnt-1]
        score = score.split("'")[0]
        score = score.replace('(',' ')
        #print(score)
        scrs=scrs+" "+score
        cnt +=1
    return(scrs)

def get_home_scorers():
    scrs = ""
    for hm_scr in stat_soup3.find_all('ul',{"sp-c-fixture__scorers-home"}):
        all_hm_scr = ""
        for hm_scr1 in hm_scr.find_all('span'):
            #hm_scr1 = hm_scr.find('span')
            hm_scr2 = hm_scr1.text.strip()
            hm_scr2 = hm_scr2.replace('\n','')
            hm_scr2 = hm_scr2.replace(' ','')
            all_hm_scr = all_hm_scr+hm_scr2
            #print(all_hm_scr)
            #print("---")
    #print(all_hm_scr)
    count = all_hm_scr.count(",")
    #print(count)
    cnt_scrs = count+1
    #print(cnt_scrs)
    cnt = 1
    #score = ""
    while cnt <= cnt_scrs:
        score = all_hm_scr.split(",")[cnt-1]
        score = score.split("'")[0]
        score = score.replace('(',' ')
        #print(score)
        scrs=scrs+" "+score
        cnt +=1
    return(scrs)

#=======================

#=======================
fix_date1 = get_fixture_date()

home_score, away_score = get_score()
#print('---------------------------------score')
#print(fix_date1)
#print(home,home_score,away,away_score)
#print('---------------------------------score')

if int(home_score) > 0:
    homescorer = get_home_scorers()
    #print(homescorer)
else:
    homescorer = []
#print("-------------------------------------3")
if int(away_score) > 0:
    awayscorer = get_away_scorers()
    #print(awayscorer)
else:
    awayscorer = []
#print("-------------------------------------4")
squad_num = []
squad_num = get_squad_num()

player_list = []
player_list, home, away = get_player_list()
print('player_list---------------------------------')
print(player_list)
#print("-------------------------------------5")
home_team = []
away_team = []

home_team, away_team = get_teams()
#print("-------------------------------------6")
# so gets a list of player surnames and full names for subs as below
# 10;Alioski ; - ', '23;Phillips ; - ', '18;Raphinha ; | Hélder Costa',
hplayer_sub = []
aplayer_sub = []
hplayer_sub,aplayer_sub = get_player_sub()
#print('aplayer_sub---------------------------------')
#print(aplayer_sub)
#print("-------------------------------------7")

home_squad = []
home_squad = get_home_squad()
#print('home_squad---------------------------------')
#print(home_squad)  

home_squad_no = [] 
home_squad_no,sqd_cnt  = get_home_squad_no()
#print('home_squad_no---------------------------------')
#print("////////////",sqd_cnt)
#print(home_squad_no)

get_subd_hsquad()
print('Home team---------------------------------')
print(hplayer_sub)
#print('Home team---------------------------------')

away_squad = []
away_squad = get_away_squad()
#print('away_squad---------------------------------')
#print(away_squad)  

away_squad_no = [] 
away_squad_no = get_away_squad_no(sqd_cnt)
#print('away_squad_no---------------------------------')
#print(away_squad_no)
#print('away_squad_no---------------------------------')

# final step gets srarting 11 plus subs
get_subd_asquad()
print('Away team---------------------------------')
print(aplayer_sub)

#=======================

# need to start builing an output line to insert into db
# always Leeds details first 

if away == "Leeds United":
    gday = fix_date1.split(" ")[0]
    gdate1 = fix_date1.split(" ")[1]
    gdate2 = fix_date1.split(" ")[2]
    gdate3 = fix_date1.split(" ")[3]
    gdate = gdate1+"-"+gdate2+"-"+gdate3
    out_line = ",A,"+away+","+away_score+","+home+","+home_score+","
    out_line = out_line+" "+(str(aplayer_sub)).replace(' ','')+'"'
    out_line = out_line+" ,'"+(str(hplayer_sub)).replace(' ','')+'"'
    out_line = out_line.replace('[','')
    out_line = out_line.replace(']','')
    out_line = out_line.replace("'",'')
    out_line = out_line.replace(";-",",0,-,0,0,-,0")
    out_line = out_line.replace(";",',')
    out_line = out_line.replace(",|",'')
    out_line = out_line.replace(",",'","')
    out_line = out_line.replace('" ",','",')
    out_line = '"'+gday+'"'+",STR_TO_DATE('"+gdate+"','%d-%M-%Y')"+out_line
    out_line = out_line.replace(')"',')')
    print("")
    print("")
    print("<===================================>")
    print(out_line)

outfile='/Users/brianellwood/football_stats/out_file.txt'
outf = open(outfile,'w')
outf.write (out_line)
outf.close()









