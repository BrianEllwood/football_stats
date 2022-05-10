
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
    # how populated in first place ?
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
    # Sep 2020 start of prem league ends may 2021
    fred = get_team_pages()
    check_fixture_list(fred)
    fixture_month_check = open('/Users/brianellwood/football_stats/fixtures_month.txt', 'r')
    fixture_number = open('/Users/brianellwood/football_stats/fixtures_number.txt', 'w')
    for line in fixture_month_check:
        line = line.replace("\n", "")
        if '/sport/football/teams/leeds-united/scores-fixtures/202' in line: # just to limit while in dev
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


# home and away team names
def get_home_away():
    cnt_1 = 1
    for link in stat_soup3.find_all('abbr'):
        if cnt_1 == 1:
            home = link.attrs['title']
        elif cnt_1 == 2:
            away = link.attrs['title']
        cnt_1 += 1
    return home,away


#  gets the score for home and away
def get_score():
    for home_score in stat_soup3.find('span',{"sp-c-fixture__number sp-c-fixture__number--home sp-c-fixture__number--ft"}):
        home_score = home_score.replace('\n','')
        home_score = home_score.replace(' ','')
    for away_score in stat_soup3.find('span',{"sp-c-fixture__number sp-c-fixture__number--away sp-c-fixture__number--ft"}):
        away_score = away_score.replace('\n','')
        away_score = away_score.replace(' ','')
    return home_score,away_score 

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
        scrs=scrs+" "+score
        cnt +=1
    scrs2 = count_ply_goals(scrs) 
    return(scrs2)

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
    scrs2 = count_ply_goals(scrs)
    return(scrs2)
##############
# new methond below
##############
def get_game_info(goal_scorers):
    all_scripts = stat_soup3.find_all('script')
    ply_goal_record = goal_scorers
    scorer_check = ply_goal_record
    scorer_check = str(scorer_check)
    scorer_check = scorer_check.replace("[","")
    scorer_check = scorer_check.replace("]","")
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
                        booking = '-'
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
                    ply_goals = '0'
                    if ply_name in scorer_check:
                        ply_goal_record_count = len(ply_goal_record)
                        pls_gls_cnt1 = 0
                        while pls_gls_cnt1 < ply_goal_record_count:
                            ply = ply_goal_record[pls_gls_cnt1]
                            pls_gls_cnt1 +=1
                            if ply_name in ply:
                                ply_goals = ply.split(",")[1]
                                ply_goals = str(ply_goals)
                    ply_dets = HA+";"+starter+";"+squad_no+";"+ply_name+";"+ply_goals+";"+booking+";"+subbed
                    #print(ply_dets)
                    teams_squads.append(ply_dets)
                    sc_cnt_1 +=1
                #print(home_team_script)
                #print(away_team_script)
                #print(play_count)
                #teams_squads = []
    #print("^^^^^^^^^",teams_squads)
    teams_squads2 = teams_squads_trim(teams_squads)
    #print("^^^^^^^^^",teams_squads2)
    #print("^^^^^^^^^")
        #teams_squads = teams_squads2
    return(teams_squads2)

def teams_squads_trim(teams_squads):
    #print("^^^^^^^^^",teams_squads)
    teams_squads_trimd = []
    for i in teams_squads:
        if i.split(";")[3] not in str(teams_squads_trimd):
            teams_squads_trimd.append(i)
    #print("^^^^^^^^^>>>>>>>>>>",teams_squads_trimd)
    return(teams_squads_trimd)

# takes the home or away scorers and counts goals 
def count_ply_goals(scrs):
    scorer_list = scrs
    scorer_list = scorer_list.lstrip(' ')
    scorer_list_count = scorer_list.count(" ")
    ply_goal_record = []
    ply_cnt = 0
    goals = 0
    while ply_cnt <= scorer_list_count:
        scorer_list_split = scorer_list.split(" ")[ply_cnt]
        scorer_list_split2 = scorer_list_split.replace("-","") # to get around hyphon in name
        if scorer_list_split2.isalpha():
            ply = scorer_list_split
            goals = 0
        else:
            goals+=1
            ply_goals = ply+','+str(goals) 
            if len(ply_goal_record) == 0:
                ply_goal_record.append(ply_goals)
            else:
                if ply in ply_goal_record[len(ply_goal_record)-1]:
                    ply_goal_record[len(ply_goal_record)-1] = ply_goals
                else:
                    ply_goal_record.append(ply_goals)
        ply_cnt+=1
    return(ply_goal_record)

##############
# needs to be in main when created
##############
ignore_list = ('Average','Half Time','Played','Won','Chelsea', 'Burnley', 'Full Time', 'Leicester City', 'Leeds United', 
'Full Time', 'West Ham United', 'Liverpool', 'Full Time', 'Brighton & Hove Albion', 'Tottenham Hotspur',
'Drawn', 'Lost', 'Goals for', 'Goals against', 'Goal difference', 'Points', 'Manchester City', 'Manchester United', 
'Liverpool', 'Leicester City', 'West Ham United', 'Tottenham Hotspur', 'Chelsea', 'Everton', 'Aston Villa', 'Arsenal', 
'Southampton', 'Leeds United', 'Crystal Palace', 'Wolverhampton Wanderers', 'Newcastle United', 
'Burnley', 'Brighton & Hove Albion', 'Fulham', 'West Bromwich Albion', 'Sheffield United','Watford','Brentford','Norwich')

populate_fixture_list() # need to only run as needed
fixture_list=[]
get_fixture(fixture_list)

outfile='/Users/brianellwood/football_stats/out_file_new1.txt'
outf = open(outfile,'w')

for link in fixture_list:
    #if '56234684' in link:
    #if '57132105' in link:
    if '5' in link:
        home = "-"
        away = "-"
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

        home, away = get_home_away()

        goal_scorers = homescorer + awayscorer
        teams_squads = []
        teams_squads2 = []
        teams_squads2 = get_game_info(goal_scorers)


# work on output

        if away == "Leeds United":
            gday = fix_date1.split(" ")[0]
            gdate1 = fix_date1.split(" ")[1]
            gdate2 = fix_date1.split(" ")[2]
            gdate3 = fix_date1.split(" ")[3]
            gdate = gdate1+"-"+gdate2+"-"+gdate3
            out_line = '"'+gday+'"'+",STR_TO_DATE('"+gdate+"','%d-%M-%Y')"
            out_line = out_line+",A,"+away+","+away_score+","+home+","+home_score+","
            hcount = str(teams_squads2).count("H;")
            acount = str(teams_squads2).count("A;")
            hacount = len(teams_squads2)
            adummy_rec ='A;B;0;-;0;-;0'
            hdummy_rec ='H;B;0;-;0;-;0'
            aw_count = hcount
            aw_list = []
            while aw_count < hacount:
                ply_rec = teams_squads2[aw_count]
                aw_list.append(ply_rec)
                aw_count +=1
            if acount < 20:
                dummy_cnt = 20-acount
                while dummy_cnt>0 :
                    aw_list.append(adummy_rec)
                    dummy_cnt = dummy_cnt -1
            hm_cnt = 0
            while hm_cnt < hcount:
                ply_rec = teams_squads2[hm_cnt]
                aw_list.append(ply_rec)
                hm_cnt +=1
            if hcount < 20:
                dummy_cnt = 20-hcount
                while dummy_cnt>0 :
                    aw_list.append(hdummy_rec)
                    dummy_cnt = dummy_cnt -1
            out_line = out_line+str(aw_list)
            out_line = out_line.replace('[','')
            out_line = out_line.replace(']','')
            out_line = out_line+"\n"
            print("")
            print("")
            print("<===================================>")
            print(out_line)
            outf.write(out_line)


        if home == "Leeds United":
            gday = fix_date1.split(" ")[0]
            gdate1 = fix_date1.split(" ")[1]
            gdate2 = fix_date1.split(" ")[2]
            gdate3 = fix_date1.split(" ")[3]
            gdate = gdate1+"-"+gdate2+"-"+gdate3
            out_line = '"'+gday+'"'+",STR_TO_DATE('"+gdate+"','%d-%M-%Y')"
            out_line = out_line+",H,"+home+","+home_score+","+away+","+away_score+","
            hcount = str(teams_squads2).count("H;")
            acount = str(teams_squads2).count("A;")
            hacount = len(teams_squads2)
            adummy_rec ='A;B;0;-;0;-;0'
            hdummy_rec ='H;B;0;-;0;-;0'
            aw_count = hcount
            aw_list = []
            hm_cnt = 0
            while hm_cnt < hcount:
                ply_rec = teams_squads2[hm_cnt]
                aw_list.append(ply_rec)
                hm_cnt +=1
            if hcount < 20:
                dummy_cnt = 20-hcount
                while dummy_cnt>0 :
                    aw_list.append(hdummy_rec)
                    dummy_cnt = dummy_cnt -1
            while aw_count < hacount:
                #print(aw_count,aw_count)
                ply_rec = teams_squads2[aw_count]
                #print(ply_rec)
                aw_list.append(ply_rec)
                aw_count +=1
            if acount < 20:
                dummy_cnt = 20-acount
                while dummy_cnt>0 :
                    aw_list.append(adummy_rec)
                    dummy_cnt = dummy_cnt -1

            out_line = out_line+str(aw_list)
            out_line = out_line.replace('[','')
            out_line = out_line.replace(']','')
            out_line = out_line+"\n"
            print("")
            print("")
            print("<===================================>")
            print(out_line)
            outf.write(out_line)  

        
outf.close()