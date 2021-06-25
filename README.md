# football_stats

About the Project

Football Stats is a development project to gain exposure to WebOps tools and practices. Football statistics was chosen to keep it intersting 
and so far Python and Docker have been used but this will increase with the development of the project.

Built With

	Python

	Docker

	Mysql

	Nginx

Getting Started

Below are what is needed to get this project started

Prerequisities

You will need the following software and this is how to install them

	Python
		brew install python3

	Docker
		https://docs.docker.com/docker-for-mac/install/

Installation 

	1. clone the repo
		git@github.com:BrianEllwood/football_stats.git
	2. Build the docker image
		docker build -t pyfootstats3 .
	
Usage 
	
	#  docker run --rm --env-file ${PWD}/.env -v ${PWD}/src/:/code/src/  pyfootstats3

	cd foot_stats_compose
	
	docker compose up --build -d 

For further information see the Documentation (none as yet)

Roadmap

see https://github.com/BrianEllwood/football_stats/issues for open issues and proposed features