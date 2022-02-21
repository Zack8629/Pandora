# Запуск базы данных:
./Pandora
1) docker-compose build
2) docker-compose up
./Pandora/Pandora   
3) python manage.py makemigrations
5) python manage.py migrate
7) python manage.py loaddata fixture/data.json
### Что бы выгрузить данные из бд:
./Pandora/Pandora
1) python manage.py dumpdata >> fixture/data.json
