#!/bin/bash
# check already running
rebuild='n'
if [ "$(docker ps -q -f name=haproxy)" ]; then
    read -p " If you wanna re compose infra ??? [y/n]" req_rebuild
    if [ ${req_rebuild} == 'y' ] || [ ${req_rebuild} == 'Y' ]; then
        rebuild='y'
    else
        echo "Exit this script"
        exit 0
    fi
fi
download='y'
# Ask will be use local source ( or downloaded already ) 
if [ -d "Infra_FRIDAY_IRIS" ]; then
    read -p " Would you use local source ? ( or downloaded already ) [y/n]" req_redown
    if [ ${req_redown} == 'n' ] || [ ${req_redown} == 'N' ]; then
        rm -rf Infra_FRIDAY_IRIS
        echo 'We will re download'
    else
        echo "Will be compose using local source"
        download='n'
    fi
fi
if [ ${download} == 'y' ]; then
    read -p " If you are developing in Codespace ? [y/n] " in_codespace
    if [ ${in_codespace} == 'y' ] || [ ${in_codespace} == 'Y' ]; then
        git clone -b codespace --single-branch https://github.com/osamhack2020/Infra_FRIDAY_IRIS.git
    elif [ ${in_codespace} == 'n' ] || [ ${in_codespace} == 'N' ]; then
        git clone https://github.com/osamhack2020/Infra_FRIDAY_IRIS.git
    fi
fi
if ! command -v docker-compose &> /dev/null
then
    echo "Install docker-script"
    chmod +x install_docker-compose.sh
    ./install_docker-compose.sh
fi
cd Infra_FRIDAY_IRIS/database
# Delete Write permission at config file
chmod a=rx master/*.cnf slave/*.cnf
if [ ${rebuild} == 'y' ]; then
    docker-compose down -v
fi
docker-compose up -d --build
sleep 20s
docker exec -i main_master_db mysql -u dbmanager -piris friday < friday.sql
cd ../..
rm -rf Infra_FRIDAY_IRIS
