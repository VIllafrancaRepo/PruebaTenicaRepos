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

---- todos los cambios se encuentran en la rama main
//para bajar cambios
git pull origin main

//para subir cambios
git push origin main

----- comandos para crear un super usuario y entrar al admin-----
python manage.py createsuperuser
user: admin
email: prueba@prueba.com
password: admin


--correr el proyecto--
python manage.py runserver

---cargar el archivo en tu postman para hacer pruebas de funcionalidad----
se encuentra en la carpeta principal del proyecto
Pruebatecnica.postman_collection.json
