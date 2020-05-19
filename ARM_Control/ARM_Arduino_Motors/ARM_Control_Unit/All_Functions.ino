void WaitingToStart(){

    waitingToStart = true; 
    pokusu=0;   
    while(waitingToStart == true){
          IamWaitingToStartMsg();
          ReadSerial();          
          ReadCanBus();
    }              
}
//:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

void Working(){

  working= true; 
  while(working == true){
        ReadSerial();
        ReadCanBus();
        ProcessFlags();
        SendActualSpeedByBus();        
  }  
  speedActual = 0;
  md.setM1Speed(0);
  md.setM2Speed(0);  
}
//:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

void AreYouAliveMsg(){
  
  byte type = 65;
  byte dataToSend[0];
  
  CreateMessage(0,type, dataToSend, "Working");
  if(pokusu>15){
      working = false;
      Monitor.println("Wathdog");
  }
  pokusu = pokusu +1;
  
}
//:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

void IamWaitingToStartMsg(){

  if(timerFlag){
     byte type = 57;
     byte dataToSend[0];
  
          CreateMessage(0,type, dataToSend,"Waiting");
          timerFlag = false;
  }
}

void setFlags(){
  
timerFlag = true;

}

void setFlags2(){
  
timerFlag2 = true;

}

void setFlagActSpeed(){

FlagActSpeed = true;

}
//:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

void ProcessFlags(){
  
        if(timerFlag == true) {          
           accelerate();        
           outputPrint();
           AreYouAliveMsg();
           timerFlag = false;
        }
}
//:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

void accelerate(){
  
  if(0 < speedRequired){
    if(speedActual < speedRequired){speedActual= speedActual + acceleration;}
    if(speedActual > speedRequired){speedActual = speedRequired;}
  }
  if(0 > speedRequired){
    if(speedActual > speedRequired){speedActual = speedActual - acceleration;}
    if(speedActual < speedRequired){speedActual = speedRequired;}
  }
  if(0 == speedRequired){speedActual = 0;}
  
  md.setM1Speed(speedActual);
  md.setM2Speed(speedActual);

  Monitor.print("Aktualni rychlost: ");
  Monitor.println(speedActual);
}
//:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

void outputPrint(){
    
  int M1CurrentMilliamps = md.getM1CurrentMilliamps();
  int M2CurrentMilliamps = md.getM2CurrentMilliamps();
    
  SendMotorsData(M1CurrentMilliamps, M2CurrentMilliamps);
}
//:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

void breaking(bool OnOff){
  
     byte onMsg[8] = {1,0,0,0,0,0,0,0};
     byte offMsg[8] = {2,0,0,0,0,0,0,0};

     working = false;
     if(OnOff){CAN.sendMsgBuf(breaksAdrHex, 0, 8, onMsg);}     
     else{CAN.sendMsgBuf(breaksAdrHex, 0, 8, offMsg);}     
}
