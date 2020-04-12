//:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
void setup_CAN(){
  
    if(CAN.begin(CAN_500KBPS, MCP_8MHz) == CAN_OK)
    {
      Monitor.print("CAN init ok!!\r\n");
    }
    else
    {
      Monitor.print("Can init fail!!\r\n");
      while(true);
    } 
    CAN.init_Mask(0, 0, 0x3ff); // arm application filter of encoder messages
    CAN.init_Mask(1, 0, 0x3ff);
    CAN.init_Mask(2, 0, 0x3ff);
    CAN.init_Mask(3, 0, 0x3ff);
    CAN.init_Mask(4, 0, 0x3ff);
    CAN.init_Mask(5, 0, 0x3ff);
  
    CAN.init_Filt(0, 0, 0x400);
    CAN.init_Filt(1, 0, 0x401);
    CAN.init_Filt(2, 0, 0x402);
    CAN.init_Filt(3, 0, 0x410);
    CAN.init_Filt(4, 0, 0x411);
    CAN.init_Filt(5, 0, 0x450);
}

//:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
void setup_Serial(){
  
    Xbee.begin(115200);
    Monitor.begin(115200);

    delay(100);
    if(Xbee.available()){Monitor.println("Xbee is ready");}
    else{Monitor.println("Xbee is not connected");}
    
}

//:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
void setup_BinnaryOutputs(){
  
    pinMode(ledPin1, OUTPUT);
    pinMode(gndPin, OUTPUT);
    digitalWrite(gndPin, LOW);//Made it low all the time for ground
}

/************************************************************************/
void setup_DataLogger(){
  
    delay(2000);
    stopRecording();
    Monitor.println("stopRecording"); 
    delay(2000);
    startRecording();
    delay(1000);
    Monitor.println("startRecording"); 
    
}

/************************************************************************/
void startRecording(){
  
     byte stmp[8] = {1,0,0,0,0,0,0,0};
  
          CAN.sendMsgBuf(dataLoggerAdrHex, 0, 8, stmp); // Sending
          
}

/************************************************************************/
void stopRecording(){
  
     byte stmp[8] = {0,0,0,0,0,0,0,0};
  
          CAN.sendMsgBuf(dataLoggerAdrHex, 0, 8, stmp); // Sending
          
}

  
