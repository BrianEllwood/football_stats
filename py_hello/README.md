
docker build -t pyimage .

docker run -d -p 5000:5000 pyimage

curl http://localhost:5000