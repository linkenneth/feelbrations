#define LED1 24
#define LED2 26
#define LED3 28
#define LED4 30
#define LED5 32

void setup() {
  // put your setup code here, to run once:
  pinMode(LED1, OUTPUT);
  pinMode(LED2, OUTPUT);
  pinMode(LED3, OUTPUT);
  pinMode(LED4, OUTPUT);
  pinMode(LED5, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  int state_LED1 = LOW;
  int state_LED2 = LOW;
  int state_LED3 = LOW;
  int state_LED4 = LOW;
  int state_LED5 = LOW;
  
  if (Serial.available()) {
    int cmd = Serial.read();
    int state_LED1 = cmd;
    digitalWrite(LED1, state_LED1);
//      case 2:
//        state_LED2 = HIGH;
//      case 2:
//        state_LED3 = HIGH;
//      case 2:
//        state_LED4 = HIGH;
//      case 2:
//        state_LED5 = HIGH;
        
//    }
  }
}
