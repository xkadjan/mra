#define RELE_1 7
#define RELE_2 6
#define RELE_3 5
#define RELE_4 4

#include <mcp_can.h>
#include <SPI.h>
MCP_CAN CAN(10);  // bylo 5
unsigned char len = 0;
unsigned char buf[8];

//const int ledPin =  13;
void led_test()
{
  Serial.println("Starting...");
//  digitalWrite(LED, HIGH);
  delay(200);
//  digitalWrite(LED, LOW);
  delay(200);
//  digitalWrite(LED, HIGH);
  delay(200);
//  digitalWrite(LED, LOW);
  
}

void setup()  {
Serial.begin(115200);
Serial.print("Breaks lives here\n\n");
led_test();
initCan();
Serial.print("Breaks are ready\n\n");
}

void loop()   
{
    ReadCanBus();
}

//:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

void ReadCanBus(){

              if(CAN_MSGAVAIL == CAN.checkReceive()) { 
                      CAN.readMsgBuf(&len, buf); // read data,  len: data length, buf: data buf
                      if(CAN.getCanId()==848){
                          switch(buf[0]){
                                  case 0:{
                                          Serial.println("stopWorking"); // zastavi pohyb motoru
                                          stopWorking();                                          
                                          break;
                                  }
                                  case 1:{
                                          Serial.println("startBreaking");
                                          startBreaking();
                                          break;
                                  }
                                  case 2:{
                                          Serial.println("stopBreaking");
                                          stopBreaking();
                                          break;
                                  }                                  
                          }
                      }                         
              }
}

//:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

void startBreaking(){ 
   
    stopWorking();

    analogWrite(RELE_1, 0);
    analogWrite(RELE_2, 0);
    analogWrite(RELE_3, 255);
    analogWrite(RELE_4, 255);
    //digitalWrite(LED, HIGH);
    delay(2500);
    
    stopWorking();
}

//:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

void stopBreaking(){  
  
    stopWorking();

    analogWrite(RELE_1, 255);
    analogWrite(RELE_2, 255);
    analogWrite(RELE_3, 0);
    analogWrite(RELE_4, 0);
    //digitalWrite(LED, HIGH);
    delay(650);

    stopWorking();
}

//:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

void stopWorking(){  
  
    analogWrite(RELE_1, 255);
    analogWrite(RELE_2, 255);
    analogWrite(RELE_3, 255);
    analogWrite(RELE_4, 255);
    //digitalWrite(LED, LOW);

}

void initCan(){
  START_INIT:

    if(CAN.begin(CAN_500KBPS, MCP_8MHz) == CAN_OK)                   // init can bus : baudrate = 500k
    {
        Serial.println("CAN BUS Shield init ok!");
    }
    else
    {
        Serial.println("CAN BUS Shield init fail");
        Serial.println("Init CAN BUS Shield again");
        delay(100);
        goto START_INIT;
    }
  }
