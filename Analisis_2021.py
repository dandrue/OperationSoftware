# -*- coding: utf-8 -*-
#!/usr/bin/env python3.7

import sqlite3
import matplotlib.pyplot as plt
import sys



# Seleccionando Ventas por producto cada mes

meses = {0 : "%01/21", 1 : "%02/21", 2 : "%03/21", 3 : "%04/21", 4 : "%05/21", 5 : "%06/21", 6 : "%07/21", 7 : "%08/21", 8 : "%09/21", 9 : "%10/21", 10 : "%11/21", 11 : "%12/21"}
meses_s = {0 : "Enero",1 : "Febrero",2 : "Marzo",3 : "Abril",4 : "Mayo",5 : "Junio",6 : "Julio",7 : "Agosto",8 : "Septiembre",9 : "Octubre",10 : "Noviembre",11 : "Diciembre"}

# Seleccionando las ventas de cada producto y agrupandolas por mes
def VentaProductoMes():
    data = []
    for i in range(len(meses)):
        con = sqlite3.connect("costos.db")
        cursor = con.cursor()
        cursor.execute("SELECT Concepto,SUM(Entra) FROM Flujo WHERE Operacion=? AND Fecha LIKE ? GROUP BY (Concepto)",("Venta",meses[i]))
        info = cursor.fetchall()
        con.close()
        data.append(info)
        print(data)
    return data

def VentaProductoMesIn():
    mes = input("Inserte el mes a evaluar: ")
    key_list = list(meses_s.keys())
    val_list = list(meses_s.values())
    value = val_list.index(str(mes))
    inp = key_list[value]
    print(inp)
    mese = meses[inp]
    print(mese)
    data = []
    con = sqlite3.connect("costos.db")
    cursor = con.cursor()
    cursor.execute("SELECT Concepto,SUM(Entra) FROM Flujo WHERE Operacion=? AND Fecha LIKE ? GROUP BY (Concepto)",("Venta",meses[inp]))
    info = cursor.fetchall()
    con.close()
    data.append(info)
    #print(data)
    Ganancia = 0
    precio_total = 0
    precio_parcial = 0
    for i in range(len(data[0])):
        concepto = data[0][i][0]
        precio = data[0][i][1]
        precio_total = precio_total + precio
        con = sqlite3.connect("costos.db")
        cursor = con.cursor()
        cursor.execute("SELECT Ganancia_Final FROM Costos WHERE Producto=?",(concepto,))
        info = cursor.fetchone()
        if info is not None:
            info = info[0]
        con.close()
        #print(concepto, precio)
        #print(info)
        try:
            Ganancia = Ganancia + precio*((info-1)/info)
            precio_parcial = precio_parcial + precio
        except TypeError:
            pass
    print("La ganancia de ventas del mes de " + str(mes) +  "fue: " + str(format(int(Ganancia),',d')))
    Ganancia = Ganancia + PagosMes(inp)
    print("La ganancia del mes de " + str(mes) +  " fue: " + str(format(int(Ganancia),',d')))
    print("La ganancia neta es: " + str(format(int(Ganancia-1230000),',d')))
    print(str(format(int(precio_total),',d')), str(format(int(precio_parcial),',d')))

def PagosMes(j):
    con = sqlite3.connect("costos.db")
    cursor = con.cursor()
    cursor.execute("SELECT SUM(Entra) FROM Flujo WHERE Operacion=? AND Fecha LIKE ?",("Pago",meses[j]))
    info = cursor.fetchone()
    if info is not None:
        info = info[0]

    ganancia_pago = info*0.45
    #print(str(format(int(info),',d')))
    print("Ganancia pagos: " + str(format(int(info*0.45),',d')))
    con.close()
    return ganancia_pago

def VentaLocal():
    for j in range(len(meses)):
        com = 0
        data = []
        con = sqlite3.connect("costos.db")
        cursor = con.cursor()
        cursor.execute("SELECT SUM(Entra) FROM Flujo WHERE (Operacion=?) AND Fecha LIKE ?",("Venta",meses[j],))
        info = cursor.fetchall()
        con.close()

        try:
            for i in range(len(info)):
                com += info[i][0]
                print("Venta Local " + meses_s[j] + " = " + str(format(com,',d')))
                print("Comisión= " + str(format(int(com*0.05),',d')))
        except TypeError:
            pass



def VentaMes():
    data = []
    datos = []
    for i in range(len(meses)):
        con = sqlite3.connect("costos.db")
        cursor = con.cursor()
        cursor.execute("SELECT SUM(Entra) FROM Flujo WHERE (Operacion=? OR Operacion=?) AND Fecha LIKE ?",("Venta","Pago",meses[i],))
        info = cursor.fetchone()

        try:
            print(meses_s[i] + ': ' + str(format(info[0],',d')))
            datos.append(info[0])
        except TypeError:
            print(meses_s[i]+ ': ' + '0,0')
            datos.append(0)
        con.close()
        data.append(info)
    return data, datos

def Grafica():
    datos = VentaMes()[1]


def Comision():
    com = 0
    con = sqlite3.connect("costos.db")
    cursor = con.cursor()
    cursor.execute("SELECT Entra FROM Flujo WHERE Operacion=? AND Fecha LIKE ?",("Venta","%02/21",))
    info = cursor.fetchall()
    #print(info)
    con.close()
    for i in range(len(info)):
        com += info[i][0]

    #print(com*0.05)
    print("Comisión= " + str(com*0.0425))

def GastosMes():
    gastos = 0
    con = sqlite3.connect("costos.db")
    cursor = con.cursor()
    cursor.execute("SELECT Sale FROM Flujo WHERE (Operacion=? OR Operacion=?) AND Fecha LIKE ?",("Gasto","Transporte","%8/21",))
    info = cursor.fetchall()
    #print(info)
    con.close()
    for i in range(len(info)):
        gastos += info[i][0]

    #print(com*0.05)
    print("Gastos= " + str(gastos))

def CompraMes():
    compras = 0
    con = sqlite3.connect("costos.db")
    cursor = con.cursor()
    cursor.execute("SELECT Sale FROM Flujo WHERE (Operacion=? OR Operacion=?) AND Fecha LIKE ?",("Compra","Retiro","%10/21",))
    info = cursor.fetchall()
    #print(info)
    con.close()
    for i in range(len(info)):
        compras += info[i][0]
    print("Compras= " + str(compras))

def InfoMes():
    VentaMes()
    Comision()
    GastosMes()
    CompraMes()





# info = VentaMes()
# #print(info)
# mes = []
# data = []
# for i in range(len(meses_s)):
#     if info[i][0]==None:
#         data.append(0)
#     else:
#         data.append(info[i][0])
#     #mes.append(meses_s[i])
#     mes.append(meses_s[i])
# import numpy as np

# # Make a fake dataset:
#
# y_pos = np.arange(len(mes))
#
# # Create bars
# plt.grid(True)
# plt.bar(y_pos, data)
#
# # Create names on the x-axis
# plt.xticks(y_pos, mes, rotation = '90')

# # Show graphic
# plt.show()

# data = VentaProductoMes()
# productos = []
# ventas = []
# for i in range(len(data)):
#     productos.append(data[i][0])
#     ventas.append(data[i][1])
#
# print(productos)
# print(ventas)
# # plt.plot(data)
# # plt.show()
#
#
# print(data)

if __name__ == '__main__':
    globals()[sys.argv[1]]()
