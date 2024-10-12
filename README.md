# PruebaTenicaRepos
Prueba Tenica para Innovation Lab

-------comandos para instalar el proyecto-----
python3 -m venv env_PruebaTecnica
cd env_PruebaTecnica
source bin/activate
git clone https://github.com/VIllafrancaRepo/PruebaTenicaRepos.git
cd cd PruebaTenicaRepos
pip install -r requirements.txt
python manage.py migrate

----- comandos para crear un super usuario y entrar al admin-----
python manage.py createsuperuser
user: admin
email: prueba@prueba.com
password: admin


--correr el proyecto--
python manage.py runserver
