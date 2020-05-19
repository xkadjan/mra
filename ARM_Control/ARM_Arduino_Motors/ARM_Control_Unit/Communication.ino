void ReadSerial(){

    while(Xbee.available()) { 
            byte typBajt[1];
          
            Monitor.println("Reading serial");
            Xbee.readBytes(typBajt,1);
            switch(typBajt[0]){
                
                   case 83:{ // set Speed
                        Monitor.println("Seting motors speed");
                        byte BajtSpeed[4];
                        Xbee.readBytes(BajtSpeed,4);
                        speedRequired = (unsigned char)(BajtSpeed[3]) << 24 | (unsigned char)(BajtSpeed[2]) << 16 | (unsigned char)(BajtSpeed[1]) << 8 | (unsigned char)(BajtSpeed[0]);
                        break;
                   }
              
                   case 87:{ // start Working
                        byte BajtStart[1];
                        Xbee.readBytes(BajtStart,1);        
                        if(BajtStart[0]==0){
                            Monitor.println("StartWorking");
                            delay(100);
                            waitingToStart = false;
                        }
                        break;
                   }
                  
                   case 65:{ // set Acceleration
                        Monitor.println("Seting Acceleration");
                        byte BajtSpeed[4];
                        Xbee.readBytes(BajtSpeed,4);
                        acceleration = (unsigned char)(BajtSpeed[3]) << 24 | (unsigned char)(BajtSpeed[2]) << 16 | (unsigned char)(BajtSpeed[1]) << 8 | (unsigned char)(BajtSpeed[0]);
                        break;
                   }

                   case 66:{ // Breaking
                        byte BeaksONOFF[1];
                        Xbee.readBytes(BeaksONOFF,1);        
                        if(BeaksONOFF[0]==1){breaking(true);}
                        if(BeaksONOFF[0]==0){breaking(false);}
                        break;
                   }
                  
                   case 68:{ // WatchDog
                        byte WatchDog[2];
                        Xbee.readBytes(WatchDog,2);
                        if(WatchDog[0]==0){
                            working = true;
                            pokusu=0;
                            Monitor.println("I am alive");
                        }
                        break;
                   }
                   
                   case 79:{ // WatchDog
                        byte WatchDog[1];
                        Xbee.readBytes(WatchDog,1);
                        if(WatchDog[0]==1){
                            digitalWrite(dataLoggerPin, HIGH);
                            Monitor.println("DataLogger started");
                        }
                        else{            
                            digitalWrite(dataLoggerPin, LOW);
                            Monitor.println("DataLogger stopped");
                        }
                        break;
                   }

                   case 80:{ // Pause
                        //Monitor.println("Pause");
                        byte BajtPause[1];
                        Xbee.readBytes(BajtPause,1);        
                        if(BajtPause[0]==0){working = false;}
                        break;
                   }

                   case 82:{ // Restart synchro board
                        //Monitor.println("Restart synchro board");
                        byte Restart[1];
                        Xbee.readBytes(Restart,1);        
                        if(Restart[0]==1)
                        {
                        digitalWrite(ledPin1, HIGH);
                        Serial.println("Restarting of synchro board");
                        delay(500);
                        digitalWrite(ledPin1, LOW);
                        }
                        break;
                   }
          
                   default:{
                          Monitor.println("Unknow message");
                          break;
                   }
            }
      }
}
   
void CreateMessage(int dataLenght, byte type, byte data[], String monitorMsg){
  
     byte message[dataLenght+5];    //message={Start byte; Type byte; Index byte; Data[]; Check byte; End byte}
     
     message[0]= (byte)'@'; // Start byte
     message[1]= type;  // Type byte
     message[2]= (byte)dataLenght;
        
     for(int i=0;i<dataLenght;i++){message[i+3]=data[i];}
     
     message[dataLenght+3]= checkByte(data,dataLenght); //CheckSum is counted only for: Data[]+SB+TB+Index
     message[dataLenght+4]= (byte)'\n'; // End byte
     
     Xbee.write(message,dataLenght+4);
     if(monitorMsg != "NULL"){
        Monitor.print(monitorMsg + " : ");
        Monitor.write(message,dataLenght+4);
        Monitor.println("");
     } 
}

byte checkByte(byte data[],int dataLenght){
  
  byte checkByte = 0;

        for(int i=0;i<dataLenght;i++){checkByte= data[i];}
  return checkByte;
}

void SendMotorsData(int M1, int M2){
  
  byte type = 71;
  byte dataToSend[6];
    
   dataToSend[0] = M1;
   dataToSend[1] = M1 >> 8;
   dataToSend[2] = M2;
   dataToSend[3] = M2 >> 8;
   dataToSend[4] = speedActual;
   dataToSend[5] = speedActual >> 8;
   CreateMessage(6,type, dataToSend,"Motors data");
}

void ReadCanBus(){

              unsigned char len = 0;
              unsigned char buf[8];
              if(CAN_MSGAVAIL == CAN.checkReceive()) {  
                      CAN.readMsgBuf(&len, buf); // read data,  len: data length, buf: data buf
                      canId = CAN.getCanId();
                      if(canId==1024){
                          CreateMessage(len, 88, buf,"NMEA");
                          //Serial.print("NMEA:");
                          //for(int i = 0; i<len; i++){Serial.print(buf[i]);Serial.print("\t");}
                      }
                      if(canId==1040){
                          CreateMessage(len, 72, buf,"halovka");
                          //for(int i = 0; i<len; i++){Serial.print(buf[i]);Serial.print("\t");}
                      }
                      if(canId==1056){
                        if(timerFlag2){
                          CreateMessage(len, 69, buf,"encoder");
                          timerFlag2 = false;
                          }
                       
                          //for(int i = 0; i<len; i++){Serial.print(buf[i]);Serial.print("\t");}
                      }
                      if(canId==1025){
                          CreateMessage(len, 50, buf,"pps");
                          //for(int i = 0; i<len; i++){Serial.print(buf[i]);Serial.print("\t");}
                      }                           
              }      
}

void SendActualSpeedByBus(){

  if(FlagActSpeed){

  byte dataToSend[2];    
   dataToSend[0] = speedActual;
   dataToSend[1] = speedActual >> 8;
   
  CAN.sendMsgBuf(speedAdrHex, 0, 2, dataToSend);

  Monitor.print("Sending speed to can:");
  FlagActSpeed= false;
  }
  else{

   // Monitor.print("Fuck can:");
    
    }
  
}
