#include <stdlib.h>

#define MOTORS_COUNT 9
#define CLOCK_RATE pow(2, 24)

int motors[MOTORS_COUNT] = { 2, 3, 4, 5, 6, 7, 24, 28, 29 };

typedef struct event {
  unsigned long time;  // microseconds
  int motor_id;
  int new_state;
} Event;

Event schedule[MOTORS_COUNT];  // only need LOW events

int event_compare(const void *a, const void *b) {
  Event e1 = *(Event *) a;
  Event e2 = *(Event *) b;
  if (e1.time < e2.time) {
    return -1;
  } else if (e1.time == e2.time) {
    return 0;
  } else {
    return 1;
  }
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  unsigned long start = micros();
  char buffer[2];
  int i = 0;

  // turn all the motors on
  for (i = 0; i < MOTORS_COUNT; i++) {
    digitalWrite(motors[i], HIGH);
  }

  // read power levels, determine when to turn motors off
  i = 0;
  while (i < MOTORS_COUNT) {
    if (Serial.available()) {
      // Computer will send 9 power levels (0-100), one for each motor.
      // Here, calculate the duty for each motor's duty cycle based on
      // this value.
      Serial.println("Reading data from serial...");
      Serial.readBytes(buffer, 2);
      unsigned int power = atoi(buffer);
      Serial.print("Power read requested: ");
      Serial.println(power);
      unsigned long duty = (unsigned long) CLOCK_RATE * power / 100.0;
      Event event = { duty, i, LOW };  // only need LOW events
      Serial.print("Calculated duty is ");
      Serial.println(duty);
      schedule[i++] = event;
    }
  }

  qsort(schedule, MOTORS_COUNT, sizeof(Event), event_compare); 

  // run schedule to turn motors off
  for (i = 0; i < MOTORS_COUNT; i++) {
    Event event = schedule[i];
    long sleep_time = event.time - (micros() - start);
    Serial.print(event.motor_id);
    Serial.print(" stopping after ");
    Serial.println(event.time);
    if (sleep_time > 0) {
      delayMicroseconds(sleep_time);
    }

    digitalWrite(motors[event.motor_id], event.new_state);
  }
}
