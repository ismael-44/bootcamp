#!/bin/bash

# Obtener el número de contenedores
num_contenedores=5

# Bucle para cada contenedor
for ((i=1; i<=$num_contenedores; i++))
do
  # Obtener la IP y el puerto del contenedor actual
  ip_actual="192.168.0.$((i+1))"
  puerto_actual=$((5000 + i + 1))

  echo "Generando JSON desde el contenedor $i..."

  # Crear un array vacío para almacenar las URLs de los nodos
  nodes=()

  # Bucle para cada contenedor destino
  for ((j=1; j<=$num_contenedores; j++))
  do
    if [ $i -ne $j ]; then
      # Obtener la IP y el puerto del contenedor destino
      ip_destino="192.168.0.$((j+1))"
      puerto_destino=$((5000 + j + 1))

      # Construir la URL del contenedor destino
      url="http://$ip_destino:$puerto_destino"

      # Agregar la URL al array de nodos
      nodes+=("\"$url\"")
    fi
  done

  # Convertir el array de nodos a formato JSON
  nodes_json=$(IFS=, ; echo "${nodes[*]}")

  # Crear el objeto JSON final con el formato "nodes"
  json="{ \"nodes\": [$nodes_json] }"

  # Guardar el JSON en un archivo con el nombre del nodo
  archivo_json="Node$i.json"
  echo $json > $archivo_json

  echo "JSON generado desde el contenedor $i y guardado en $archivo_json"
done

