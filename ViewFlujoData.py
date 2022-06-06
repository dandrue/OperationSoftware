# -*- coding: utf-8 -*-
#!/usr/bin/env python3.7

import sqlite3
fecha = input("Introduce una fecha dd/mm/yy: ")
con = sqlite3.connect("costos.db")
cursor = con.cursor()
cursor.execute('SELECT * FROM Flujo WHERE Fecha=?',(fecha,))
info = cursor.fetchall()
print(info)
con.commit()
con.close()
