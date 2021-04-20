In $HOME/football_stats/py_dock_stats

docker build -t pyfootstats3 .

# docker run docker run --rm   pyfootstats2

docker run --rm -v ${PWD}/src/:/code/src/  pyfootstats3
