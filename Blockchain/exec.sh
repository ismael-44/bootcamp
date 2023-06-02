#!/bin/bash
clear

file_numb=$(ls /jsons/* | wc | awk '{print $1}')
connect(){
	for ((i = 1; i <= file_numb; i++)); do
		ip=$((i + 1))
		echo $ip
  		curl -X POST -H "Content-Type: application/json" -d "@/jsons/node_$i.json" http://172.20.0.$ip:500$ip/connect_node 
	done
}

mine_block() {
    echo "Mining block for Node $selected_node..."
	curl http://172.20.0.$selected_ip:500$selected_port/mine_block | jq
}

show_chain() {
    echo "Showing chain for Node $selected_node..."
	curl http://172.20.0.$selected_ip:500$selected_port/chain | jq
}

verify_chain() {
    echo "Verifying chain for Node $selected_node..."
	echo "$selected_ip $selected_port"
	curl http://172.20.0.$selected_ip:500$selected_port/verify | jq
}

update_chains(){
	for ((i=1; i<=file_numb; i++)); do
		ip=$((i + 1))
		curl http://172.0.0.$ip:500$ip/replace_chain | jq
	done

}

echo "Welcome to the 42 Coin administration panel!"
read -p "Enter the node you want to operate on (Node 1-10): " selected_node
selected_ip=$((selected_node + 1))
selected_port=$((selected_node + 1))
while true; do
    echo
    echo "Node $selected_node Menu:"
    echo "1. Mine Block"
    echo "2. Show Chain"
    echo "3. Verify Chain"
    echo "4. Select a different node"
	echo "5. Connect all nodes"
	echo "6. Replace chain"
    echo "7. Exit"
    read -p "Enter your choice (1-7): " option
    
    case $option in
        1)
            mine_block
            ;;
        2)
            show_chain
            ;;
        3)
            verify_chain
            ;;
        4)
            read -p "Enter the node you want to operate on (Node 1-9): " selected_node
			selected_ip=$((selected_node + 1))
			selected_port=$((selected_node + 1))
            ;;
		5)
			connect
			;;
		6)
			update_chains
			;;
		7)
            echo "Exiting the program. Goodbye!"
            exit 0
            ;;
        *)
            echo "Invalid option. Please select a valid option."
            ;;
    esac
done
