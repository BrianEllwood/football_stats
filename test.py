#teams_squads = ['H;S;1;Fabianski;0;-;90', 'H;S;5;Coufal;0;-;90', 'H;S;15;Dawson;1;-;90', 'H;S;23;Diop;0;-;90', 'H;S;3;Cresswell;0;-;90', 'H;S;28;Soucek;0;-;90', 'H;S;41;Rice;0;-;90', 'H;S;18;Fornals;0;-;90', 'H;S;11;Lingard;1;Y;87', 'H;B;31;Johnson;0;-;3', 'H;S;9;Benrahma;0;-;73', 'H;B;20;Bowen;0;-;17', 'H;S;30;Antonio;0;-;90', 'H;B;4;Balbuena;0;-;0', 'H;B;10;Lanzini;0;-;0', 'H;B;16;Noble;0;-;0', 'H;B;20;Bowen;0;-;0', 'H;B;25;Martin;0;-;0', 'H;B;31;Johnson;0;-;0', 'H;B;34;Trott;0;-;0', 'H;B;45;Odubeko;0;-;0', 'A;S;1;Meslier;0;-;90', 'A;S;2;Ayling;0;-;90', 'A;S;14;Llorente;0;-;90', 'A;S;6;Cooper;0;-;90', 'A;S;15;Dallas;0;-;90', 'A;S;23;Phillips;0;Y;90', 'A;S;17;Hélder Costa;0;-;45', 'A;B;22;Harrison;0;-;45', 'A;S;11;Roberts;0;-;60', 'A;B;20;Rodrigo;0;-;30', 'A;S;43;Klich;0;-;45', 'A;B;10;Alioski;0;-;45', 'A;S;18;Raphinha;0;-;90', 'A;S;9;Bamford;0;-;90', 'A;B;7;Poveda-Ocampo;0;-;0', 'A;B;10;Alioski;0;-;0', 'A;B;20;Rodrigo;0;-;0', 'A;B;22;Harrison;0;-;0', 'A;B;24;Davis;0;-;0', 'A;B;25;Caprile;0;-;0', 'A;B;28;Berardi;0;-;0', 'A;B;47;Jenkins;0;-;0', 'A;B;52;Huggins;0;-;0']
teams_squads  = ['H;S;1;Meslier;0;-;90', 'H;S;2;Ayling;0;-;90', 'H;S;14;Llorente;0;-;90', 'H;S;21;Struijk;0;-;90', 'H;S;10;Alioski;0;Y;90', 'H;S;23;Phillips;0;-;90', 'H;S;18;Raphinha;0;-;90', 'H;S;15;Dallas;0;-;90', 'H;S;11;Roberts;0;Y;90', 'H;S;22;Harrison;0;-;64', 'H;B;17;Hélder Costa;0;-;26', 'H;S;9;Bamford;0;-;35', 'H;B;20;Rodrigo;0;Y;44', 'H;B;43;Klich;0;-;11', 'H;B;5;Koch;0;-;0', 'H;B;7;Poveda-Ocampo;0;-;0', 'H;B;13;Casilla;0;-;0', 'H;B;17;Hélder Costa;0;-;0', 'H;B;20;Rodrigo;0;-;0', 'H;B;28;Berardi;0;-;0', 'H;B;43;Klich;0;-;0', 'H;B;46;Shackleton;0;-;0', 'H;B;47;Jenkins;0;-;0', 'A;S;16;Mendy;0;-;90', 'A;S;28;Azpilicueta;0;-;90', 'A;S;4;Christensen;0;-;90', 'A;S;2;Rüdiger;0;-;90', 'A;S;21;Chilwell;0;-;90', 'A;S;7;Kanté;0;-;90', 'A;S;5;Jorginho;0;-;90', 'A;S;10;Pulisic;0;-;68', 'A;B;24;James;0;-;22', 'A;S;22;Ziyech;0;-;69', 'A;B;11;Werner;0;-;21', 'A;S;19;Mount;0;-;79', 'A;B;20;Hudson-Odoi;0;-;11', 'A;S;29;Havertz;0;-;90', 'A;B;1;Arrizabalaga;0;-;0', 'A;B;3;Alonso;0;-;0', 'A;B;11;Werner;0;-;0', 'A;B;15;Zouma;0;-;0', 'A;B;17;Kovacic;0;-;0', 'A;B;18;Giroud;0;-;0', 'A;B;20;Hudson-Odoi;0;-;0', 'A;B;24;James;0;-;0', 'A;B;33;Emerson;0;-;0']


team_trim = []
for i in teams_squads:
    if i.split(";")[3] not in str(team_trim):
        team_trim.append(i)

hcount = str(team_trim).count("H;")
acount = str(team_trim).count("A;")
hacount = len(team_trim)
adummy_rec ='A;B;0;-;0;-;0'
hdummy_rec ='H;B;0;-;0;-;0'

aw_count = hcount
aw_list = []

hm_cnt = 0
while hm_cnt < hcount:
    ply_rec = team_trim[hm_cnt]
    aw_list.append(ply_rec)
    hm_cnt +=1
if hcount < 20:
    dummy_cnt = 20-hcount
    while dummy_cnt>0 :
        aw_list.append(hdummy_rec)
        dummy_cnt = dummy_cnt -1

while aw_count < hacount:
    #print(aw_count,aw_count)
    ply_rec = team_trim[aw_count]
    #print(ply_rec)
    aw_list.append(ply_rec)
    aw_count +=1
if acount < 20:
    dummy_cnt = 20-acount
    while dummy_cnt>0 :
        aw_list.append(adummy_rec)
        dummy_cnt = dummy_cnt -1


print(aw_list)
tmp1 = len(aw_list)
print("-------")
print(hacount,hcount,acount,tmp1)
print("39 19 20")

