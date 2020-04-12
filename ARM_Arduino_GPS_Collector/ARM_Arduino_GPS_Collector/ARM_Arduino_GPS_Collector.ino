#include <SPI.h>
#include <SD.h>
#include "TimerThree.h"

int               ledPin1 = A12;
int               ledPin2 = A13;
int               ledPin3 = A14;
int               ledPin0 = A15;
int               buzzPin = A11;
int               gndPin = A10;

File              sdFile;

String            fileName_S0 = "S0_log.txt";
String            fileName_S1 = "S1_log.txt";
String            fileName_S2 = "S2_log.txt";
String            fileName_S3 = "S3_log.txt";

char              inputChar_S0 = 0;
char              inputChar_S1 = 0;
char              inputChar_S2 = 0;
char              inputChar_S3 = 0;

String            inputString_S0 = "";
String            inputString_S1 = "";
String            inputString_S2 = "";
String            inputString_S3 = "";
 
unsigned long     timerLED_S0;
unsigned long     timerLED_S1;
unsigned long     timerLED_S2;
unsigned long     timerLED_S3;

String            nmea = "$GNGGA,091830.00,5007.77480,N,01422.50159,E,1,10,1.04,296.3,M,44.3,M,,*4B";

void setup()
{
  setup_PINS();
  test_Indicators(5);
  setup_Serial();
  //setup_SD();
  //create_files();  
  Timer3.initialize(1000000);   // po 1ms vyvola preruseni
  Timer3.attachInterrupt(send_fixed_poss);
}
 
void loop()
{
  /*process_S0();
  process_S1();
  process_S2();
  process_S3();*/  
  delay(5);
}


