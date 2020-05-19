void setup_CAN(){
  
    if(CAN.begin(CAN_500KBPS, MCP_8MHz) == CAN_OK){Serial.print("CAN init ok!!\r\n");}
      else {Serial.print("Can init fail!!\r\n");} // Pridat upozorneni, ze can nefunguje a zastavit to
}
   

void setup_GNSS(){
  /*gpsOnBoard.begin(115200);
  delay(200);
  gpsOnBoard.println("$PMTK251,9600*17");
  delay(200);*/
  gpsOnBoard.begin(9600);
  delay(200);
  gpsOnBoard.println("$PMTK251,115200*1F");
  delay(200); 
  gpsOnBoard.begin(115200);
  //delay(100);
  //gpsOnBoard.println("$PMTK251,9600*17");
  //gpsOnBoard.println("$PMTK251,115200*1F");
  //delay(100);
  //gpsOnBoard.begin(9600);
  delay(100);
  if (filter == 0)
  {
    gpsOnBoard.println("$PMTK314,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0*29");// Set GPS to send both GGA messages
  }
  if (filter == 1)
  {
    gpsOnBoard.println("$PMTK314,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0*29"); // send RMC
  }
  delay(100);
  gpsOnBoard.println("$PMTK220,100*2F");                   // Set GPS to update its position status every 100 ms
  delay(100);
  gpsOnBoard.println("$PMTK300,1000,0,0,0,0*1C");           // Set GPS to send its position status over serial port every 200 ms
  gpsOnBoard.flush();
  delay(100);

  
  char temp;
  long testTimerGNSS = millis();
  report("uTime of GNNS init");
  report(micros()); 
  while (!gps.time.isUpdated()){    //wait for gps to init
        if (millis() > 3000+testTimerGNSS){
           Serial.println("GNSS not found!");
           GNSSisOk = false;
           return;
        }
        if (gpsOnBoard.available())
        {
        char tmp = gpsOnBoard.read();
        
             Serial.print(tmp);
             gps.encode(tmp);          
            
        }
    }
  report("\nGPS available");
  
}


/*void setup_GNSS2(){
 
  gpsOnBoard.begin(9600);
  delay(200);
  gpsOnBoard.println("$PMTK251,115200*1F");
  delay(200); 
  gpsOnBoard.begin(115200);
  //delay(100);
  //gpsOnBoard.println("$PMTK251,9600*17");
  //gpsOnBoard.println("$PMTK251,115200*1F");
  //delay(100);
  //gpsOnBoard.begin(9600);
  delay(100);
  if (filter == 0)
  {
    gpsOnBoard.println("$PMTK314,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0*29");// Set GPS to send both GGA messages
  }
  if (filter == 1)
  {
    gpsOnBoard.println("$PMTK314,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0*29"); // send RMC
  }
  delay(100);
  gpsOnBoard.println("$PMTK220,100*2F");                   // Set GPS to update its position status every 100 ms
  delay(100);
  gpsOnBoard.println("$PMTK300,1000,0,0,0,0*1C");           // Set GPS to send its position status over serial port every 200 ms
  gpsOnBoard.flush();
  delay(100);

  
  char temp;
  long testTimerGNSS = millis();
  report("uTime of GNNS init");
  report(micros()); 
  int cntr = 0;
  while (!gps.time.isUpdated()){    //wait for gps to init
        if (millis() > 3000+testTimerGNSS){
           Serial.println("GNSS not found!");
           GNSSisOk = false;
           return;
        }
        if (gpsOnBoard.available())
        {
             temp = gpsOnBoard.read();
             gps.encode(temp);
             report(cntr);            
             inputNMEA_GNSS_Buffer += temp;
            
              if (cntr == 17 && inputNMEA_GNSS_Buffer[0] == '$')
              {
                 inputNMEA_GNSS_Time = "";
                 
                 for (int x = 7; x < 17; x++)
                 { inputNMEA_GNSS_Time += inputNMEA_GNSS_Buffer[x]; }
                 
                 sendStringData(0x400,inputNMEA_GNSS_Time);
                 report(inputNMEA_GNSS_Time);
                 inputNMEA_GNSS_Buffer = "";
                      
              }
            cntr += 1;
            
        }
    }
  report("\nGPS available");
  
}
*/
void setup_PINS(){
    
      pinMode(FIX_PIN, INPUT_PULLUP);
      pinMode(HALL_PIN, INPUT_PULLUP);
      pinMode(ENCA_PIN, INPUT_PULLUP);
      pinMode(ENCB_PIN, INPUT_PULLUP);
      pinMode(LED_PIN_red, OUTPUT);
      pinMode(LED_PIN_blue, OUTPUT);
      //Timer3.attachInterrupt(timerLED).start(LED_BLINK_INTERVAL*1000);
      pinMode(LED_BUILTIN, OUTPUT);

      pinMode(LED_PIN_PPS, OUTPUT);
      pinMode(LED_PIN_HALL, OUTPUT);
      pinMode(LED_PIN_ENC, OUTPUT);
      
}

void timerLED(){
  digitalWrite(LED_PIN_sensor, LOW);
  digitalWrite(LED_PIN_PPS, LOW);
  digitalWrite(LED_PIN_HALL, LOW);
  digitalWrite(LED_PIN_ENC, LOW);
  //Timer3.stop();
}

void setup_LED(){
  Timer3.attachInterrupt(timerLED).start(LED_BLINK_INTERVAL*1000);
  Timer3.start();
  delay(200);
  blinkLED(400);
  blinkLED(410);
  blinkLED(420);
}

void setup_DataLogger(){
  
    stopRecording();
    delay(2000);
    startRecording();
    delay(1000);
}


void waitToGetFix(){
  
  int FixPortLightingTime = 0;
  while(FixPortLightingTime<3000){
      if(!digitalRead(FIX_PIN)){
        FixPortLightingTime=FixPortLightingTime+50;
        delay(50);
        }
        else{FixPortLightingTime=0;}   
    } 
  }


