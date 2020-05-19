inline void getFirstPPS(){ attachInterrupt(digitalPinToInterrupt(PPS_PIN), handleFirstPPS, RISING);}

/************************************************************************/
void handleFirstPPS(){
  
  ppsTime = micros();  
  PPSFlag = true;
}

/************************************************************************/
inline void enableInterruptPPS(){ attachInterrupt(digitalPinToInterrupt(PPS_PIN), handlePPS, RISING);}

/************************************************************************/
void handlePPS(){
  
  ppsTime = micros();
  ++ppsNumber;  
  PPSFlag = true;
}

/********* Halova sonda ***************************************************************/
inline void enableInterruptHall(){
  
  pinMode(HALL_PIN, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(HALL_PIN), handleHall, RISING);
}

/************************************************************************/
void handleHall(){
  if ( micros() - HallTime > 500000 ){
    HallTime = micros();
    ++HallNumber;
    HallFlag = true;
  }
}

/******* ENCODER *****************************************************************/
void enableInterruptEncoder() {
  
  pinMode(ENCA_PIN, INPUT);           // set pin to input
  pinMode(ENCB_PIN, INPUT);           // set pin to input
  
  digitalWrite(ENCA_PIN, HIGH);       // turn on pullup resistors
  digitalWrite(ENCB_PIN, HIGH);       // turn on pullup resistors

  attachInterrupt(ENCA_PIN, updateEncA, RISING);
//attachInterrupt(ENCB_PIN, updateEncB, RISING);
}

/************************************************************************/
void updateEncA() {
  
  if(digitalRead(ENCB_PIN)==LOW){
      EncoderNumber++;
      EncoderTime=micros();
      }
    else{
      EncoderNumber--;
      EncoderTime=micros();
      }
    EncoderFlag = true;
}

/************************************************************************/
void updateEncB() {
  
  if(digitalRead(ENCA_PIN)==LOW){
      EncoderNumber--;
      EncoderTime=micros();
  }
  else{
      EncoderNumber++;
      EncoderTime=micros();
  }
  EncoderFlag = true;
}
