from multiprocessing import connection
from plistlib import UID
import pwd
import pyodbc

server = 'localhost'
bd = 'SOX_PIGUE_SA'
user = 'sa'
password = '#SQLserver2022'


try:
    connection = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server}; SERVER='+server+'; DATABASE='+bd+';UID='+user+'; pwd='+password+';TrustServerCertificate=yes;')
    print('conexion exitosa')

except Exception as ex:
    print(ex)

#Consulta a la base de datos.

cursor = connection.cursor()
#cursor.execute('Select cod_articu from STA11;')
#SELECT DESCRIPCIO, DESC_ADIC, COD_ARTICU FROM STA11 WHERE DESCRIPCIO LIKE 'DE160C%'
#cursor.execute("SELECT CANT_STOCK FROM STA19 WHERE COD_ARTICU = 'S10111104500002' ")
cursor.execute("SELECT DESCRIPCIO, DESC_ADIC, COD_ARTICU FROM STA11 WHERE DESCRIPCIO LIKE 'DE160C%' ")

articulos = cursor.fetchall()

for articulo in articulos:
    print(articulo)



cursor.close()
connection.close()