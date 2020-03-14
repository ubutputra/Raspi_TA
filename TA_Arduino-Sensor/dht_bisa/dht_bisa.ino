#include "DHT.h" //library sensor yang telah diimportkan 
#define DHTPIN A2     //Pin apa yang digunakan
#define DHTTYPE DHT11   // DHT 11
DHT dht(DHTPIN, DHTTYPE);

#include <SPI.h>                  /* to handle the communication interface with the modem*/
#include <nRF24L01.h>             /* to handle this particular modem driver*/
#include <RF24.h>                 /* the library which helps us to control the radio modem*/

#define pot_pin A0                /*Variable pin of POT is to be connected to analog pin 0 i.e.A0*/
RF24 radio(8,7);                    /* Creating instance 'radio'  ( CE , CSN )   CE -> D7 | CSN -> D8 */                              
const byte Address[6] = "00009";     /* Address to which data to be transmitted*/

void setup() {
  // put your setup code here, to run once:

  Serial.begin(9600); //baud komunikasi serial
  Serial.println("Pengujian DHT11!"); //penulisan di serial monitor
  dht.begin(); //prosedur memulai pembacaan module sensor
  
//  pinMode(pot_pin,INPUT);         /* Setting A0 (POT pin) as input*/
  radio.begin ();                 /* Activate the modem*/
  radio.openWritingPipe (Address); /* Sets the address of transmitter to which program will send the data */
}
 
void loop() {
  // put your main code here, to run repeatedly:
  delay(500);  //menunggu beberapa detik untuk pembacaan
 
  //pembacaan sensor membutuhkan waktu 250ms
 
  //Pembacaan untuk data kelembaban
  float humidity_1 = dht.readHumidity();
  //Pembacaan dalam format celcius (c)
  float celcius_1 = dht.readTemperature();
  //pembacaan dalam format Fahrenheit
  float fahrenheit_1 = dht.readTemperature(true);
 
  //mengecek pembacaan apakah terjadi kegagalan atau tidak
  if (isnan(humidity_1) || isnan(celcius_1) || isnan(fahrenheit_1)) {
    Serial.println("Pembacaan data dari module sensor gagal!");
    return;
  }
 
  float htof = dht.computeHeatIndex(fahrenheit_1, humidity_1); 
  //Prosedur pembacaaan data indeks panas dalam bentuk fahreheit
  float htoc = dht.computeHeatIndex(celcius_1, humidity_1, false);
 //Prosedur pembacaaan data indeks panas dalam bentuk celcius
 
  //pembacaan nilai pembacaan data kelembaban
  Serial.print("Kelembaban: ");
  Serial.print(humidity_1);
  Serial.print(" %\t");
  
  //pembacaan nilai pembacaan data suhu
  Serial.print("Suhu : ");
  Serial.print(celcius_1); //format derajat celcius
  Serial.print(" 'C ");
  Serial.print(fahrenheit_1); //format derajat fahrenheit
  Serial.print(" 'F\t");
 
  Serial.print("Indeks Panas: ");
  Serial.print(htof); 
  Serial.println(" *F");
 
  Serial.print(htoc);
  Serial.print(" *C ");
  
  radio.stopListening ();          /* Setting modem in transmission mode*/
//  int value = analogRead(pot_pin);    /*Reading analog value at pin A0 and storing in varible 'value'*/
  int value = celcius_1;
  int data = map( value , 0 , 1023 , 0 , 255 );   /* Convering the 10 bit value to 8 bit */
//  radio.write(&data, sizeof(data));            /* Sending data over NRF 24L01*/
  radio.write(&value, sizeof(value));            /* Sending data over NRF 24L01*/

  Serial.print("Transmitting Data : ");
  Serial.println(value);      
}
 
