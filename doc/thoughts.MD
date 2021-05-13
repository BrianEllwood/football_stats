
# Start with an H1 heading

Ok not much of a doco but more where to put thoughts before i forget on what i am doing/done and where to go

so currently i have pyhton script to scrape information on a football result
the steps

1 go to the first url and get the url for leeds
 https://www.bbc.co.uk/sport/football/teams/leeds-united/scores-fixtures

2 from here the season
 http_scores_fixtures  = "https://www.bbc.co.uk/sport/football/teams/leeds-united/scores-fixtures" 

3 this has a url for each result and fixture. 
 http_scores_fixtures  = "https://www.bbc.co.uk/sport/football/teams/leeds-united/scores-fixtures/2021-01" 

4 this is where i will be scrapping the information i am interested in unique id for each result
 http_scores_fixtures  = "https://www.bbc.co.uk/sport/football/55769208"

5 As this script is under development i did not want to be hitting the website every time i re ran the script.
so the url in 4 i did a  one off scrape, which i used BeautifulSoup to write to a file, which i then use to test my 
script against.

 result  = requests.get(http_scores_fixtures)

 result.status_code

 rcontents = result.content

 stat_soup = BeautifulSoup(rcontents, 'html.parser')

 rawfile='/Users/brianellwood/football_stats/page.dat'
 rf = open(rawfile,'w')
 rf.write (stat_soup.prettify())
 rf.close()