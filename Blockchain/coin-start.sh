#!/bin/bash

read -p "How many node will the coin have? Maximum 9 nodes" node_len

if [ $node_len -gt 9 ]; then
	echo "To many nodes, use less nodes"
	exit
fi

node_len=$((node_len + 2))
echo $node_len > test.txt

docker network create --subnet=172.20.0.0/16 coin
docker rm -f $(docker ps -aq)
docker rmi -f $(docker images -aq)
for ((i = 2; i < node_len; i++)); do
	node_num=$((5000 + i))
    filename="node$((i)).py"
    cp criptomonea.py "$filename"
	sed -i '' 's/port = "5000"/port = "'"$node_num"'"/' $filename
    echo "FROM python" > Dockerfile
	echo "RUN python3 -m pip install flask" >> Dockerfile
	echo "RUN python3 -m pip install requests" >> Dockerfile
    echo "COPY $filename /$filename" >> Dockerfile
    echo "CMD python3 /$filename" >> Dockerfile
docker build -t $i .
docker run -p $node_num:$node_num --network coin --ip 172.20.0.$i -d $i
rm Dockerfile
rm $filename
done
rm node*
contenedores=$(docker ps -aq | wc | cut -d " " -f 8)
for ((i=1; i<=$contenedores; i++))
do
  ip_actual="172.20.0.$((i+1))"
  puerto_actual=$((5000 + i + 1))

  nodes=()
  for ((j=1; j<=$contenedores; j++))
  do
    if [ $i -ne $j ]; then
      ip_destino="172.20.0.$((j+1))"
      puerto_destino=$((5000 + j + 1))
      url="http://$ip_destino:$puerto_destino"
      nodes+=("\"$url\"")
    fi
  done
  nodes_json=$(IFS=, ; echo "${nodes[*]}")
  json="{ \"nodes\": [$nodes_json] }"
  archivo_json="node_$i.json"
  echo $json > $archivo_json
done
echo "FROM python" > Dockerfile
echo "COPY exec.sh /exec.sh" >> Dockerfile
echo "RUN mkdir /jsons" >> Dockerfile
echo "COPY node* /jsons/" >> Dockerfile
echo "RUN apt update && apt install -y jq" >> Dockerfile
echo "CMD bash /exec.sh" >> Dockerfile
docker build -t panel .
docker run -it --network coin --ip 172.20.0.50 panel



