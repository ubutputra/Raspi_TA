import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import time
import spidev
import mysql.connector


def insert_db(data):
    mydb = mysql.connector.connect(
      host="167.71.211.175",
      user="ubut",
      passwd="ubut31",
      database="db_ta"
    )
    
    mycursor = mydb.cursor()

    sql = "INSERT INTO data_sensor (id_node,data_mq7,data_mq135,data_dht11_temperature,data_dht11_humidity,created_at) VALUES (%s, %s,%s,%s,%s,%s)"
    val = data
    print(val)
    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")    



GPIO.setmode(GPIO.BCM)
pipes = [[0xF0, 0xF0, 0xF0, 0xF0, 0xA1], [0xF0, 0xF0, 0xF0, 0xF0, 0xA2], [0xF0, 0xF0, 0xF0, 0xF0, 0xB4]]
pipes2 = [[0xE8, 0xE8, 0xF0, 0xF0, 0xE1], [0xF0, 0xF0, 0xF0, 0xF0, 0xE1]]


radio = NRF24(GPIO, spidev.SpiDev())
radio.begin(0, 17)

radio.setPayloadSize(32)
radio.setChannel(0x76)
radio.setDataRate(NRF24.BR_1MBPS)
radio.setPALevel(NRF24.PA_MIN)

radio.setAutoAck(True)
radio.enableDynamicPayloads()
radio.enableAckPayload()

radio.openReadingPipe(1, pipes[0])
radio.openReadingPipe(2, pipes[1])
radio.printDetails()

radio.startListening()
count = 0 
while True:
    while not radio.available(0):
        print("belum ada data yang masuk")
        time.sleep(1 / 1000)
    
    

    if (radio.available(pipes[0])):
        print("pipes 1 - node 1 >>>>>")
        print(pipes[0])
    if (radio.available(pipes[1])):
        print("pipes 2 - node 2 >>>>>")        
        receivedMessage = []
        radio.read(receivedMessage, radio.getDynamicPayloadSize())
        print(radio.getDynamicPayloadSize())
        print(receivedMessage)
        print("Received: {}".format(receivedMessage))
        print("Translating the receivedMessage into unicode characters")
        string = ""
        for n in receivedMessage:
            # Decode into standard unicode set
            if (n >= 32 and n <= 126):
                string += chr(n)
        print(string)
        data = string.split("|")
        datetime = time.strftime('%Y-%m-%d %H:%M:%S')
        data = list(map(int,data))
        data.append(datetime)
        print("list integer : {}".format(data))
        insert_db(data)


        count = count + 1
        print("received message decodes to : {}".format(string))
        print("data ke {}".format(count))
        print(datetime)
        print("-->><<--")
    
