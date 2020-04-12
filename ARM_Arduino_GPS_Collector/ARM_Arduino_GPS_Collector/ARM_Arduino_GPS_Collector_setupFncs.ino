void setup_PINS(){
  pinMode(ledPin1, OUTPUT);
  pinMode(ledPin2, OUTPUT);
  pinMode(ledPin3, OUTPUT);
  pinMode(ledPin0, OUTPUT);
  pinMode(buzzPin, OUTPUT);
  pinMode(gndPin, OUTPUT);
  digitalWrite(gndPin, LOW);//Made it low all the time for ground
}
void test_Indicators(int num){
  for (int i=0; i < num; i++){
    digitalWrite(ledPin1, HIGH);
    digitalWrite(ledPin2, HIGH);
    digitalWrite(ledPin3, HIGH);
    digitalWrite(ledPin0, HIGH);
    digitalWrite(buzzPin, HIGH);
    delay(100);
    digitalWrite(ledPin1, LOW);
    digitalWrite(ledPin2, LOW);
    digitalWrite(ledPin3, LOW);
    digitalWrite(ledPin0, LOW);
    digitalWrite(buzzPin, LOW);
    delay(100);
  }
}
void setup_Serial(){
  Serial.begin(115200);
  Serial1.begin(115200);
  Serial2.begin(115200);
  Serial3.begin(115200);
}
void setup_SD(){
    Serial.print("Initializing SD card... ");

  if (!SD.begin(8)){
    Serial.println("failed!");
    test_Indicators(50);
    return;
  }
  Serial.println("done.");
}
void send_fixed_poss()
{
 Serial.println(nmea);
 Serial1.println(nmea);
 Serial2.println(nmea);
 Serial3.println(nmea);
}

