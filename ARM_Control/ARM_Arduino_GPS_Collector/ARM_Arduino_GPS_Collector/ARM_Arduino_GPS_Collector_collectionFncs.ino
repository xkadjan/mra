void process_S0(){  
  while (Serial.available()) {
    inputChar_S0 = (char)Serial.read();
    inputString_S0 += inputChar_S0;
    if (inputChar_S0 == '\n') {
      sdFile = SD.open(fileName_S0, FILE_WRITE);
      sdFile.print(inputString_S0);
      sdFile.close();
      inputString_S0 = "";
      digitalWrite(ledPin0, HIGH);
      timerLED_S0 = millis();
      Serial.print("S0");
    }
  }
  if (timerLED_S0 < millis() - 20) digitalWrite(ledPin0, LOW);
}

void process_S1(){  
  while (Serial1.available()) {
    inputChar_S1 = (char)Serial1.read();
    inputString_S1 += inputChar_S1;
    if (inputChar_S1 == '\n') {
      sdFile = SD.open(fileName_S1, FILE_WRITE);
      sdFile.print(inputString_S1);
      sdFile.close();
      inputString_S1 = "";
      digitalWrite(ledPin1, HIGH);
      timerLED_S1 = millis();
      Serial.print("S1");
    }
  }
  if (timerLED_S1 < millis() - 20) digitalWrite(ledPin1, LOW);
}
void process_S2(){  
  while (Serial2.available()) {
    inputChar_S2 = (char)Serial2.read();
    inputString_S2 += inputChar_S2;
    if (inputChar_S2 == '\n') {
      sdFile = SD.open(fileName_S2, FILE_WRITE);
      sdFile.print(inputString_S2);
      sdFile.close();
      inputString_S2 = "";
      digitalWrite(ledPin2, HIGH);
      timerLED_S2 = millis();
      Serial.print("S2");
    }
  }
  if (timerLED_S2 < millis() - 20) digitalWrite(ledPin2, LOW);
}
void process_S3(){  
  while (Serial3.available()) {
    inputChar_S3 = (char)Serial3.read();
    inputString_S3 += inputChar_S3;
    if (inputChar_S3 == '\n') {
      sdFile = SD.open(fileName_S3, FILE_WRITE);
      sdFile.print(inputString_S3);
      sdFile.close();
      inputString_S3 = "";
      digitalWrite(ledPin3, HIGH);
      timerLED_S3 = millis();
      Serial.print("S3");
    }
  }
  if (timerLED_S3 < millis() - 20) digitalWrite(ledPin3, LOW);
}
void create_files(){
  create_file(fileName_S0);
  create_file(fileName_S1);
  create_file(fileName_S2);
  create_file(fileName_S3);
}
void create_file(String fileName)
{
  sdFile = SD.open(fileName, FILE_WRITE);
  sdFile.println("     ... NEW MEASUREMENT: " + String(fileName) + " ...");
  sdFile.close();
  Serial.println(" - the file " + fileName + " has been created!");
}
