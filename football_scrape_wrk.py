
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup

import requests

import os.path

# function definitions

def get_team_pages():
    http_scores_fixtures  = "https://www.bbc.co.uk/sport/football/teams/leeds-united/scores-fixtures" 
    result  = requests.get(http_scores_fixtures)
    rcontents = result.content
    stat_soup = BeautifulSoup(rcontents, 'html.parser')
    return(stat_soup)

def check_fixture_list(stat_soup):
    # checks for the list of fixtures if not there populates it
    if os.path.isfile('/Users/brianellwood/football_stats/fixtures_month.txt') != True:
        fixture_month = open('/Users/brianellwood/football_stats/fixtures_month.txt', 'w')
        for link in stat_soup.find_all('a'):
            alink = link.get('href')
            if 'leeds-united/scores-fixtures/20' in alink:
                fixture_month.write(alink+ '\n')
        fixture_month.close()
    return()

def populate_fixture_list():
    # takes the fixture_month and get each game url for that month
    fixture_month_check = open('/Users/brianellwood/football_stats/fixtures_month.txt', 'r')
    fixture_number = open('/Users/brianellwood/football_stats/fixtures_number.txt', 'w')
    for line in fixture_month_check:
        line = line.replace("\n", "")
        if '/sport/football/teams/leeds-united/scores-fixtures/2021-03' in line: # just to limit while in dev
            line = 'https://www.bbc.co.uk'+line
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
    return()

def get_fixture(fixture_list):
    # checks for file containg fixures then puts into list
    if os.path.isfile('/Users/brianellwood/football_stats/fixtures_number.txt') == True:
        fixture_number = open('/Users/brianellwood/football_stats/fixtures_number.txt', 'r')
        for line in fixture_number:
            line = line.replace('\n',"")
            fixture_list.append(line)
        fixture_number.close()
    return(fixture_list)

def get_fixture_soup(link):
    result2  = requests.get(link)
    if result2.status_code == 200:
        rcontents2 = result2.content
        # i did the dev work on this from a file created using prettify 
        # if i run the scrape directly against stat_soup3 = BeautifulSoup(rcontents2, 'html.parser')
        # it fails hence the steps below to prettify then parse again.
        stat_soup3 = BeautifulSoup(rcontents2, 'html.parser') 
        stat_soup4 = stat_soup3.prettify()
        stat_soup = BeautifulSoup(stat_soup4, 'html.parser') 
    else:
        print("status code",result2.status_code)
    return stat_soup

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

# gets a the lists of hame and away players and used subs.     
def get_player_sub():
    cnt_3 = 0
    hcnt_4 = 0
    hcnt_player_list = 0
    acnt_4 = 0
    acnt_player_list = 0
    for strt_player in player_list:
        if home_team[0].split(";")[1] in  player_list[cnt_3]:
            hcnt_player_list = cnt_3+1 ### so goal keeper was man of match so appeared twice at begining of list is mom always first ?
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
                else:
                    prev_cnt = (hcnt_4 - 1)
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
                    pl_sub = away_team[acnt_4]+" "+goals+" ; - " 
                    aplayer_sub.append(pl_sub)
                    acnt_4 +=1
                    acnt_player_list +=1   
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
        cnt_7 +=1
    return home_squad_no,cnt_7

def get_away_squad_no(sqd_cnt):
    cnt_7 = sqd_cnt
    cnt_8 = 0
    for aplayer in away_squad:
        goals = "0" 
        aplayer_sq = squad_num[cnt_7]+" ; "+away_squad[cnt_8]+" "+goals
        away_squad_no.append(aplayer_sq)
        cnt_7 +=1
        cnt_8 +=1
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
            aw_scr2 = aw_scr1.text.strip()
            aw_scr2 = aw_scr2.replace('\n','')
            aw_scr2 = aw_scr2.replace(' ','')
            all_aw_scr = all_aw_scr+aw_scr2
    count = all_aw_scr.count(",")
    cnt_scrs = count+1
    cnt = 1
    while cnt <= cnt_scrs:
        score = all_aw_scr.split(",")[cnt-1]
        score = score.split("'")[0]
        score = score.replace('(',' ')
        print("<>",score)
        scrs=scrs+" "+score
        cnt +=1
    return(scrs)

def get_home_scorers():
    scrs = ""
    for hm_scr in stat_soup3.find_all('ul',{"sp-c-fixture__scorers-home"}):
        all_hm_scr = ""
        for hm_scr1 in hm_scr.find_all('span'):
            hm_scr2 = hm_scr1.text.strip()
            hm_scr2 = hm_scr2.replace('\n','')
            hm_scr2 = hm_scr2.replace(' ','')
            all_hm_scr = all_hm_scr+hm_scr2
    count = all_hm_scr.count(",")
    cnt_scrs = count+1
    cnt = 1
    while cnt <= cnt_scrs:
        score = all_hm_scr.split(",")[cnt-1]
        score = score.split("'")[0]
        score = score.replace('(',' ')
        scrs=scrs+" "+score
        cnt +=1
    return(scrs)
##############
# new methond below
##############
def get_game_info():
    all_scripts = stat_soup3.find_all('script')

    for number, script in enumerate(all_scripts):
            script_string = script.string
            if  "homeTeam" in script_string and "lineFormationPosition" in script_string:   
                squad_script = (all_scripts[number].string)
                ply_cnt = squad_script.count("status")
                home_team_script = squad_script.split('homeTeam')[1]
                squad_script=squad_script.replace('"uniformNumber":', '')
                home_team_script = squad_script.split('homeTeam')[1]
                home_team_script = home_team_script.split(':')[2]
                away_team_script = squad_script.split('awayTeam')[1]
                play_count = away_team_script.count("status")
                away_team_script = away_team_script.split(':')[2]
                sc_cnt_1 = 1
                ply_goals = '0'
                while ply_cnt >= sc_cnt_1 :
                    if sc_cnt_1 <= (ply_cnt - play_count):
                        HA = "H"
                    else:
                        HA = "A"
                    player_info = squad_script.split('status')[sc_cnt_1]
                    col1 = player_info.split('":"')[1]
                    col1 = col1.replace('"','')
                    starter = col1.split(',')[0]
                    starter = starter.replace('"','')
                    squad_no = col1.split(',')[1]
                    ply_name = player_info.split('abbreviation')[1]
                    ply_name = ply_name.split(',')[0]
                    
                    booking = player_info.split('bookings')[1]
                    booking = booking.split(',')[0]
                    if 'yellow' in booking:
                        booking = 'Y'
                    if 'red' in booking:
                        booking = 'R'
                    if booking == '":[]':
                        booking = ' '
                    if starter == 'starter':
                        starter = 'S'
                    else:
                        starter = 'B'
                    subbed = player_info.split('substitutions')[1]
                    if "replacedBy" in subbed :
                        subbed = subbed.split('timeElapsed')[1]
                        subbed = subbed.split(',')[0]
                        subbed = subbed.replace('":','')
                    else :
                        if starter == 'S':
                            subbed = '90'
                        else:
                            subbed = '0'
                    if 'timePlayedTotal' in player_info:
                        subbed = player_info.split('timePlayedTotal')[1]
                        subbed = subbed.split('}')[0]
                        subbed = subbed.replace('":','')
                        subbed = subbed.replace('"','')
                    squad_no = squad_no.replace('}','')
                    ply_name = ply_name.replace('}','')
                    ply_name = ply_name.replace('"','')
                    ply_name = ply_name.replace(':','')
                    #print("|",ply_name,"|",awayscorer)
                    if ply_name in homescorer:
                        print("home scorer")
                    if ply_name in awayscorer:
                        print("awy scorer")
                    ply_dets = HA+";"+starter+";"+squad_no+";"+ply_name+";"+ply_goals+";"+booking+";"+subbed
                    #print(ply_dets)
                    teams_squads.append(ply_dets)
                    sc_cnt_1 +=1
                #print(home_team_script)
                #print(away_team_script)
                #print(play_count)
                #teams_squads = []
    return(teams_squads)


##############
# needs to be in main when created
##############
ignore_list = ('Average','Half Time','Played','Won','Chelsea', 'Burnley', 'Full Time', 'Leicester City', 'Leeds United', 
'Full Time', 'West Ham United', 'Liverpool', 'Full Time', 'Brighton & Hove Albion', 'Tottenham Hotspur',
'Drawn', 'Lost', 'Goals for', 'Goals against', 'Goal difference', 'Points', 'Manchester City', 'Manchester United', 
'Liverpool', 'Leicester City', 'West Ham United', 'Tottenham Hotspur', 'Chelsea', 'Everton', 'Aston Villa', 'Arsenal', 
'Southampton', 'Leeds United', 'Crystal Palace', 'Wolverhampton Wanderers', 'Newcastle United', 
'Burnley', 'Brighton & Hove Albion', 'Fulham', 'West Bromwich Albion', 'Sheffield United')

# This just reads from fixtures_number.txt
fixture_list=[]
#get_fixture(fixture_list)
linez = 'https://www.bbc.co.uk/sport/football/57034891'
fixture_list.append(linez)
for link in fixture_list:
    #if '56234684' in link:
    print(link)
    if '57034891' in link:
        home = "-"
        away = "-"
        # currently the only hit on the BBC
        stat_soup3=get_fixture_soup(link)
        
        fix_date1 = get_fixture_date()

        home_score, away_score = get_score()
        if int(home_score) > 0:
            homescorer = get_home_scorers()
        else:
            homescorer = []
        if int(away_score) > 0:
            awayscorer = get_away_scorers()
        else:
            awayscorer = []

        print(fix_date1,home,away,home_score,homescorer,away_score,awayscorer)

        teams_squads = []
        get_game_info()
        print(teams_squads)

        #squad_num = []
        #squad_num = get_squad_num()

        #player_list = []
        #player_list, home, away = get_player_list()
        
        #home_team = []
        #away_team = []
        #home_team, away_team = get_teams()
        
        #hplayer_sub = []
        #aplayer_sub = []
        #hplayer_sub,aplayer_sub = get_player_sub()
        
        #home_squad = []
        #home_squad = get_home_squad()
        
        #home_squad_no = [] 
        #home_squad_no,sqd_cnt  = get_home_squad_no()

        #get_subd_hsquad()
        #print('Home team---------------------------------')
        #print(hplayer_sub)

        #away_squad = []
        #away_squad = get_away_squad() 

        #away_squad_no = [] 
        #away_squad_no = get_away_squad_no(sqd_cnt)

        # final step gets srarting 11 plus subs
        #get_subd_asquad()
        #print('Away team---------------------------------')
        #print(aplayer_sub)
