void getGNSSTimeInPPSpulse() {
  bool NMEAreaded = false;

  report("getGNSSTimeInPPSpulse running");
  while (!NMEAreaded) {                   // dokud nenacte NMEA s PPS
    while (!PPSFlag) {}                     // Ceka na PPS puls
    while (gpsOnBoard.available()) {      //pokusi se nacist NMEA, kdyz neni validni ceka na dalsi pulse
      NMEAChar = (char)gpsOnBoard.read();
      inputNMEA_GNSS_Buffer += NMEAChar;
      if (NMEAChar == '\n') {
        NMEAreaded = filterGGARMC(filter);
      }
    }
  }
}

void getGNSSTimeInPPSpulse2() {

  report("getGNSSTimeInPPSpulse running");

  String temppp;
  int startt = millis();

  while (gpsOnBoard.available())
  {
    temppp += (char)gpsOnBoard.read();
    //report(gpsOnBoard.available());
    //report("in while loop");
    if (millis() - startt > 20000)
    {
      break;
    }
  }
  gpsOnBoard.flush();
  report(gpsOnBoard.available());
  report(temppp);
}


void sendStringData(int adrHex, String DataString) {

  byte myStringByte[9];
  int bytesToCopy = 0;

  for (; DataString.length() > 0;) {
    if (DataString.length() > 8) {
      bytesToCopy = 8; // max of bytes in one message is 8 bytes
    }
    else {
      bytesToCopy = DataString.length();
    }

    DataString.getBytes(myStringByte, bytesToCopy + 1); // Copy from String to 8Byte array
    CAN.sendMsgBuf(adrHex, 0, bytesToCopy, myStringByte); // Sending
    DataString.remove(0, bytesToCopy); // Remove sent bytes from String
  }
}


void sendLongData(int adrHex, long number) {

  byte buf[4];

  buf[3] = number;
  buf[2] = number >> 8;
  buf[1] = number >> 16;
  buf[0] = number >> 24;

  CAN.sendMsgBuf(adrHex, 0, 4, buf); // Sending
}


void startRecording() {
  byte stmp[8] = {1, 0, 0, 0, 0, 0, 0, 0};
  CAN.sendMsgBuf(DataLoggerAdrHex, 0, 8, stmp); // Sending
}


void stopRecording() {
  byte stmp[8] = {0, 0, 0, 0, 0, 0, 0, 0};
  CAN.sendMsgBuf(DataLoggerAdrHex, 0, 8, stmp); // Sending
}


void getPPSSynchroTime() {

  waitToGetFix();
  getFirstPPS();
  emptySerialBuffer();

  enableInterruptPPS();
  readFirstNMEAs2();

  sendLongData(0x401, ppsTime);
  sendStringData(0x400, inputNMEA_GNSS_Time); //inputNMEA_GNSS_Time
  sendLongData(0x402, ppsNumber);

  /*report("NMEA sent to logger:");
    report(inputNMEA_GNSS_Time);
    report("PPStime sent to logger:");
    report(ppsTime);*/

}

void blinkLED(int numOfLED) {
  if (numOfLED == 400) {
    digitalWrite(LED_PIN_PPS, HIGH);
  }
  if (numOfLED == 410) {
    digitalWrite(LED_PIN_HALL, HIGH);
  }
  if (numOfLED == 420) {
    digitalWrite(LED_PIN_ENC, HIGH);
  }
  //Timer3.start();
}

/*
  void readFirstNMEAs()
  {
   report("readFirstNMEAs running");
   int runs = 0;
   while(runs < 5)
    {
      //report(runs);
      delay(1);

      if(PPSFlag)
        {
          //report(runs);
          //report(ppsTime);
          inputNMEA_GNSS_Time = "";
          runs++;
          bool NMEAreaded = false;
          while(!NMEAreaded)
              { // dokud nenacte NMEA s PPS

                  while(gpsOnBoard.available())
                      {               //pokusi se nacist NMEA, kdyz neni validni ceka na dalsi pulse
                          //NMEAChar = (char)gpsOnBoard.read();
                          //inputNMEA_GNSS_Buffer += NMEAChar;
                          inputNMEA_GNSS_Buffer += (char)gpsOnBoard.read();
                          if (NMEAChar == '\n')
                              {
                                NMEAreaded = filterGGARMC(filter);
                              }

                      }
            }
    }
  }
  }
*/
/*
  void parseNMEA()
  {
   bool NMEAreaded = false;


   while(!NMEAreaded){ // dokud nenacte NMEA s PPS



        while(gpsOnBoard.available())
        {
              NMEAChar = (char)gpsOnBoard.read();
              inputNMEA_GNSS_Buffer += NMEAChar;
              if (NMEAChar == '\n')
                {
                  NMEAreaded = filterGGARMC(filter);
                }
        }


   }
  }
*/

void emptySerialBuffer()
{
  // vyprazdneni RX bufferu na Serial 3

  while (gpsOnBoard.available())
  {
    gpsOnBoard.read();
  }
}


bool filterGGARMC(int filter)
{

  if (filter == 0)
  {
    if (inputNMEA_GNSS_Buffer[3] == 'G' && inputNMEA_GNSS_Buffer[4] == 'G' && inputNMEA_GNSS_Buffer[5] == 'A') {
      inputNMEA_GNSS_Time = "";
      for (int x = 7; x < 17; x++) {
        inputNMEA_GNSS_Time += inputNMEA_GNSS_Buffer[x];
      }
      //NMEAreaded = true;
      PPSFlag = false;
      //report(inputNMEA_GNSS_Time);
      inputNMEA_GNSS_Buffer = "";
      return true;
    }
  }
  if (filter == 1)
  {
    if (inputNMEA_GNSS_Buffer[3] == 'R' && inputNMEA_GNSS_Buffer[4] == 'M' && inputNMEA_GNSS_Buffer[5] == 'C') {
      inputNMEA_GNSS_Time = "";
      for (int x = 7; x < 17; x++) {
        inputNMEA_GNSS_Time += inputNMEA_GNSS_Buffer[x];
      }
      //NMEAreaded = true;
      PPSFlag = false;
      report(inputNMEA_GNSS_Time);
      inputNMEA_GNSS_Buffer = "";
      return true;
    }
  }


}


/*void printValidTime()
  {

  if (gps.time.isUpdated())
  {

    Serial.print(gps.time.hour()); Serial.print(F(":"));
    Serial.print(gps.time.minute()); Serial.print(F(":"));
    Serial.print(gps.time.second()); Serial.print(F("."));
    Serial.println(gps.time.centisecond());
  }
  else
  {
    Serial.println("Time invalid");
  }
  }
*/

bool filterGGA()
{
  // vraci true to NMEAreaded
  // parsuje GGA zpravu a plni inputNMEA_GNSS_Time casem v GGA zprave

  if (inputNMEA_GNSS_Buffer[3] == 'G' && inputNMEA_GNSS_Buffer[4] == 'G' && inputNMEA_GNSS_Buffer[5] == 'A') {

    for (int x = 7; x < 17; x++) {
      inputNMEA_GNSS_Time += inputNMEA_GNSS_Buffer[x];
    }

    PPSFlag = false;

    return true;
  }




}

void readFirstNMEAs2()
{

  //vycita 4 GGA zpravy

  report("readFirstNMEAs2 running");
  int runs = 0;
  while (runs < 5)
  {
    inputNMEA_GNSS_Time = "";
    inputNMEA_GNSS_Buffer = "";

    if (PPSFlag)
    {
      runs++;
      bool NMEAreaded = false;
      while (!NMEAreaded)
      {
        while (gpsOnBoard.available())
        {
          NMEAChar = (char)gpsOnBoard.read();
          inputNMEA_GNSS_Buffer += NMEAChar;
          if (NMEAChar == '\n')
          {
            //report(inputNMEA_GNSS_Buffer);
            NMEAreaded = filterGGA();
          }

        }
      }
    }
  }
}

