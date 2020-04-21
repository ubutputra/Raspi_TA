import mysql.connector

mydb = mysql.connector.connect(
  host="167.71.211.175",
  user="ubut",
  passwd="ubut31",
  database="db_ta"
)

mycursor = mydb.cursor()

sql = "INSERT INTO Data_Sensor (ppm_co, temp,humidity) VALUES (%s, %s,%s)"
val = ("3","4","8")
mycursor.execute(sql, val)

mydb.commit()

print(mycursor.rowcount, "record inserted.")
