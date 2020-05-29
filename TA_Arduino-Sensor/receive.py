import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import time
import spidev
import mysql.connector


def insert_db(data):
    mydb = mysql.connector.connect(
      host="128.199.246.173",
      user="ubut",
      passwd="sukolilo10",
      database="db_ta_ubut2016"
    )
    
    mycursor = mydb.cursor()

    sql = "INSERT INTO data_sensor (id_node,data_mq7,data_dht11_temperature,data_dht11_humidity,data_mq135,created_at) VALUES (%s, %s,%s,%s,%s,%s)"
    val = data
    #print(val)
    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")    



GPIO.setmode(GPIO.BCM)
pipes = [[0xF0, 0xF0, 0xF0, 0xF0, 0xA1], [0xF0, 0xF0, 0xF0, 0xF0, 0xA2], [0xF0, 0xF0, 0xF0, 0xF0, 0xA3]]


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
radio.openReadingPipe(3, pipes[2])
radio.printDetails()

radio.startListening()
count = 0 
while True:
    while not radio.available(0):
        #print("belum ada data yang masuk")
        time.sleep(1 / 5000)
        
    
   

    if (radio.available()):
        print("Data Node Sensor Masuk >>>>>")
        receivedMessage = []
        radio.read(receivedMessage, radio.getDynamicPayloadSize())
        print(radio.getDynamicPayloadSize())
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
        if(data[0] == 1):
            print("Data dari node sensor 1")
        if(data[0] == 2):
            print("Data dari node sensor 2")
        if(data[0] == 3):
            print("Data dari node sensor 3")        
        data.append(datetime)
        print("list integer : {}".format(data))
        insert_db(data)


        count = count + 1
        #print("received message decodes to : {}".format(string))
        print("data ke {}".format(count))
        print(datetime)
        print("-->><<--")
    
