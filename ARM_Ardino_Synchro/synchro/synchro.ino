#include <mcp_can.h>
#include <TinyGPS++.h>
#include <DueTimer.h>

#define report(x) Serial.println(x)
#define gpsOnBoard Serial3
#define LED_BLINK_INTERVAL 20 //ms

MCP_CAN CAN(5);
TinyGPSPlus   gps;


const int     FIX_PIN = 8;  //8
const int     PPS_PIN = 4; //4
bool          PPSFlag = true;
unsigned long ppsTime = 0;
unsigned long ppsNumber = 0;

const int     HALL_PIN = 6;
unsigned long HallTime = 0;
unsigned long HallNumber = 0;
bool          HallFlag = false;

const int     ENCA_PIN = 2;
const int     ENCB_PIN = 3;
unsigned long EncoderTime = 0;
         long loggedEncoderNumber = 0;
volatile int  EncoderNumber = 0;
bool          EncoderFlag = false;
int           encoderResolution = 1;

String        inputNMEA_GNSS_Buffer = "";
String        inputNMEA_GNSS_Time = "";
bool          GNSSisOk = true;
char          NMEAChar;
const int     LED_PIN_red = 10; //senzor
const int     LED_PIN_blue = 11;

const int     LED_PIN_sensor = 10;
const int     LED_PIN_record = 11;

const int     LED_PIN_PPS = A0;
const int     LED_PIN_HALL = A1;
const int     LED_PIN_ENC = A2;

int           DataLoggerAdrHex = 0x300;
int           i;
int           filter = 0; // 0 -- filter GGA, 1 -- filter RMC

//::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
void setup() {

  Serial.begin(9600);

  setup_CAN();
  setup_GNSS();
  setup_PINS();
  setup_LED();
  setup_DataLogger();

  getPPSSynchroTime();
  
  enableInterruptHall();
  enableInterruptEncoder();


}

//::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
void loop() {

  if (PPSFlag) {
  
      sendLongData(0x401, ppsTime);
      sendLongData(0x402, ppsNumber);
      PPSFlag = false;
      blinkLED(400);
  }

  if (HallFlag) {
      sendLongData(0x410, HallTime);
      sendLongData(0x411,HallNumber);
      HallFlag = false;
      blinkLED(410);
  }

  if (EncoderFlag) {
      if(abs(loggedEncoderNumber-EncoderNumber) >= encoderResolution){ 
         sendLongData(0x420, EncoderTime);
         sendLongData(0x421, EncoderNumber);
         EncoderFlag = false;
         loggedEncoderNumber=EncoderNumber;
         blinkLED(420);
      }
  }
}
