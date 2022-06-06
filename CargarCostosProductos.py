import pandas as pd
import sqlite3
from sqlite3 import *
from sqlite3 import Error

file_name = "COSTOS_ACTUALIZADO.xlsx"
sheet = "Costos"


con = sqlite3.connect("costos.db")
cursor = con.cursor()
print("Eliminando datos anteriores")
cursor.execute('DELETE FROM Costos')
con.commit()

df = pd.read_excel(io=file_name, sheet_name=sheet)
for i in range(len(df)):
    if i!=0:
        cod = df.iloc[i,0]
        prod = df.iloc[i,1]
        costo = df.iloc[i,2]
        gan = df.iloc[i,3]
        precio = df.iloc[i,4]
        precio_venta = float(df.iloc[i,5])
        gan_final = df.iloc[i,6]
        peso = df.iloc[i,7]
        DataProducto = [cod, prod, costo, gan, precio, precio_venta, gan_final, peso]

        con = sqlite3.connect("costos.db")
        cursor = con.cursor()
        print("Cargando {} a base de datos".format(str(prod)))
        cursor.execute('INSERT INTO Costos(Codigo, Producto, Costo, Ganancia, Precio, Precio_Venta,Ganancia_Final, Peso) VALUES(?,?,?,?,?,?,?,?)', DataProducto)
        con.commit()
        con.close()
