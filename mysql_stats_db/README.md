Prerequisites 
--------------
in $HOME/football_stats

mkdir -p mysql_stats_db/mysql-datadir

is this needed at if pulling repo dir structure would be there ?

To create mysql container

docker run \
--detach \
--name=stats-db-mysql \
--env="MYSQL_ROOT_PASSWORD=some_password" \
--publish 6603:3306 \
--volume=$HOME/football_stats/mysql_stats_db/conf.d:/etc/mysql/conf.d \
--volume=$HOME/football_stats/mysql_stats_db/mysql-datadir:/var/lib/mysql \
mysql

initial connect to mysql

mysql  -uroot -psome_password -h localhost -P 6603 --protocol=tcp

mysql> CREATE DATABASE stats_db;

for subsequent connections 

mysql  stats_db -uroot -psome_password -h localhost -P 6603 --protocol=tcp

At this point i created the table matchday and inserted a test row

As this is still POC thats ok but i think all required tables should be built some how.