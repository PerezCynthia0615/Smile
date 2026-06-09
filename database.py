#Esta es nuestra conexión con MongoDB, donde vamos a colocar la URL que nos da la página. 

from pymongo import MongoClient
#Tienes que instalar pymongo desde la terminal, ingresa "pip install pymongo" y listo. 

client = MongoClient("mongodb+srv://Cynthia:PHCJ190579@proyectophcj.o0cpph4.mongodb.net/?appName=ProyectoPHCJ")

#Aquí va el nombre de su base de datos. 
# Cambia el guion medio (-) por un guion bajo (_)
db = client['SMILE_DENTISTA']