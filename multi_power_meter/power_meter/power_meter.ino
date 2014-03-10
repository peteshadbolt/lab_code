


int i=0;
int j=0;
long values[6] = {0, 0, 0, 0, 0, 0};
int pins[6] = {A0, A1, A2, A3, A4, A5};
int integration_steps=10;

void setup() {
  Serial.begin(9600); 
}

void loop() {
  for (j=0; j<6; j++){values[j]=0;}
  
  for (i=0; i<integration_steps; i++) {
     for (j=0; j<6; j++){values[j]+=analogRead(pins[j]);}
     delay(1);
  }
 
  for (j=0; j<6; j++){
    Serial.print(values[j]);
    if(j<5){Serial.print(",");}
  }
  
  Serial.print("\n");
}

