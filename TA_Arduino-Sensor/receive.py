import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import time
import spidev

GPIO.setmode(GPIO.BCM)


address = [[0xe7, 0xe7, 0xe7, 0xe7, 0xe7], [C,O,B,A]]
pipes = [[0xE8, 0xE8, 0xF0, 0xF0, 0xE1], [0xF0, 0xF0, 0xF0, 0xF0, 0xE1] ]

radio = NRF24(GPIO, spidev.SpiDev())
radio.begin(0, 17)

radio.setPayloadSize(32)
radio.setChannel(0x76)
radio.setDataRate(NRF24.BR_1MBPS)
radio.setPALevel(NRF24.PA_MIN)

radio.setAutoAck(True)
radio.enableDynamicPayloads()
radio.enableAckPayload()

#radio.openReadingPipe(1, pipes[1])
radio.openReadingPipe(1, address[1])
radio.printDetails()

radio.startListening()
count = 0 
while True:
    ackPL = [1]
    while not radio.available(0):
        time.sleep(1 / 1000)
    receivedMessage = []
    radio.read(receivedMessage, radio.getDynamicPayloadSize())
    print(receivedMessage)
    print("Received: {}".format(receivedMessage))
    print("Translating the receivedMessage into unicode characters")
    string = ""
    for n in receivedMessage:
        # Decode into standard unicode set
        if (n >= 32 and n <= 126):
            #print(n)
            string += chr(n)
    print(string)
    #radio.writeAckPayload(1, ackPL, len(ackPL))
    #print("Loaded payload reply of {}".format(ackPL))
    count = count + 1
    print("received message decodes to : {}".format(string))
    print("pesan ke {}".format(count))
    print(time.strftime('%X %x %Z'))
    print("-->><<--")
    
