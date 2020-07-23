void setup() {
  Serial.begin(9600);
  pinMode(2,OUTPUT);
  pinMode(3,OUTPUT);
  pinMode(4,OUTPUT);
  pinMode(5,OUTPUT);
  digitalWrite(2,LOW);
  digitalWrite(3,LOW);
  digitalWrite(4,LOW);
  digitalWrite(5,LOW);
  analogWrite(11,35);
  analogWrite(10,45);
  ;
  while (Serial.available()==0){
    //Serial.print("hi");
  }
}
char a='F';
void loop() {
  
  //a=Serial.read();
  if(a=='F')
  { Serial.print('F'); 
    digitalWrite(3,HIGH);
     digitalWrite(5,HIGH);
  }
  else if(a=='R') 
  { 
    digitalWrite(3,HIGH);
    digitalWrite(5,LOW);
    digitalWrite(4,HIGH);
  }
  else if(a=='L')
  { 
    digitalWrite(2,HIGH);
    digitalWrite(3,LOW);
    digitalWrite(5,HIGH);}

  
    
  else if (a=='S')
  {
  
    digitalWrite(3,HIGH);
     digitalWrite(5,HIGH);
  digitalWrite(2,LOW);
  digitalWrite(4,LOW);
  digitalWrite(5,LOW);
  digitalWrite(3,LOW);
  }
}
