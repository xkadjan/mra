#include "DualVNH5019MotorShield.h"
#include <mcp_can.h>    // CAN shield for DUE
#include <DueTimer.h>   // Timer for DUE
#define Xbee Serial1
#define Monitor Serial    // debug

DualVNH5019MotorShield md;
MCP_CAN CAN(5);

bool          waitingToStart = true;
bool          working = true;

bool          timerFlag = false;
bool          timerFlag2 = false;
bool          FlagActSpeed = false;

int           pokusu = 0;
int           speedRequired = 0;
int           acceleration = 1;
int           speedActual = 0;
int           dataLoggerPin = 7;
int           dataLoggerAdrHex = 0x300;
int           breaksAdrHex = 0x350;
int           speedAdrHex = 0x450;

int           ledPin1 = A11;
int           gndPin = A10;

int canId;
//:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

void setup(){ 
  setup_BinnaryOutputs(); 
  setup_Serial();
  setup_CAN();
  md.init();                                // initilization of motor shield
  Timer2.attachInterrupt(setFlagActSpeed).start(100000);
  Timer3.attachInterrupt(setFlags).start(100000);
  Timer4.attachInterrupt(setFlags2).start(100000);
}
//:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

void loop(){
  Monitor.println("Monitor of MotorShield"); 
  Monitor.println("Measurement ARM is waiting to start"); 
  WaitingToStart();
  Monitor.println("WORKING"); 
  Working();
  Monitor.println("STOPPED"); 
}
