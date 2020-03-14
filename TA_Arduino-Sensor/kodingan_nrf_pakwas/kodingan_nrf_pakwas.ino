#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

RF24 radio(7, 8);

const int nodeID=1;
const int chId=1;
const int statusCH=0;
const int rxAddr = 5000;
const int rxAddr1 = 2000;
const int rxAddr2 = 3000;
const int rxAddr3 = 4000;
int sendAddr3 = 5000;


int a = 0, xMili = 0, xSecond = 0, xMinute = 0, xHour = 0, currentSecond = 0, currentMilis=0;
unsigned long wTime;
int flag = 1;
void setup()
{

  xMili = 0; xSecond = 0; xMinute = 0; xHour = 0;


  while (!Serial);
  Serial.begin(9600);


  radio.begin();
  radio.openReadingPipe(0, rxAddr);
  radio.startListening();

}


void countTime() {
  if (xMili == 999) {
    ++xSecond;
    xMili = 0;
  }
  if ((xSecond > 59)) {
    ++xMinute;
    xSecond = 0;
    currentSecond = -1;
  }
  if (xMinute > 59) {
    ++xHour;
    xMinute = 0;

  }
  ++xMili;
}

void countMillis() {
 
  wTime=millis();
  if (currentMilis==0){
    currentMilis=wTime;
  }
  
  if ((wTime - currentMilis > 999)) {
    ++xSecond;
    currentMilis = wTime;
  }
  if ((xSecond > 59)) {
    ++xMinute;
    xSecond = 0;
    currentSecond = -1;
  }
  if (xMinute > 59) {
    ++xHour;
    xMinute = 0;

  }
 // ++xMili;
}


void tapListening() {

  // radio.openReadingPipe(0, rxAddr);
  // radio.startListening();

  if (radio.available())
  {
    // int a = 0;
     char rtext[25];
    radio.read(&rtext, sizeof(rtext));
    //Serial.println("Pesannya ?");
    
    //main IF
    // kode pesan = rText[1];
  //  jika pesan == C
   //  (adress kirim diganti ke 
    Serial.println(rtext);
  }
}

void transmit(String Message)
{

  radio.setRetries(15, 15);
  radio.stopListening();
  radio.openWritingPipe(rxAddr);

  String c = Message;
  char pesan[25];
  c.toCharArray(pesan, 25);

  int  rNumber  = random(1,5);
  delay(rNumber);
  
  radio.write(&pesan, sizeof(pesan));
  radio.openReadingPipe(0, rxAddr);
  radio.startListening();


}




void transmit(int sendAddr, String Message)
{

  radio.setRetries(15, 15);
  radio.stopListening();
  radio.openWritingPipe(rxAddr);

  String c = Message;
  char pesan[25];
  c.toCharArray(pesan, 25);

  int  rNumber  = random(1,5);
  delay(rNumber);
  
  radio.write(&pesan, sizeof(pesan));
  radio.openReadingPipe(0, sendAddr);
  radio.startListening();


}


void loop()
{



  currentSecond = xSecond;
  countMillis();


  tapListening();

   

   
    if (((xSecond % 3) == 0)&& (flag=1)) {

    char text[25];
    String myMessage = String(xHour, DEC) + ":" + String(xMinute, DEC) + ":" + String(xSecond, DEC);
    
     myMessage.concat("#ryanda_bgst#" );
     transmit(myMessage);
      Serial.println(myMessage);
    }       
 
  
   
  delay(1000);
}
