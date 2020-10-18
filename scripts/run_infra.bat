@echo off
git clone https://github.com/osamhack2020/Infra_FRIDAY_IRIS.git
cd Infra_FRIDAY_IRIS/database
attrib +R master/*.cnf
attrib +R slave/*.cnf
docker-compose down -v
docker volume rm database_db_backup
docker-compose up -d --build
TIMEOUT /T 20 /NOBREAK
docker exec -i main_master_db mysql -u dbmanager -piris friday < friday.sql
cd ../..
rmdir /s /q Infra_FRIDAY_IRIS
pause
