#include "gps.h"
#include <TinyGPS++.h>
#include <SoftwareSerial.h>
static TinyGPSPlus gps;
static SoftwareSerial gpsSerial(4, 3);
void initGps() {
  gpsSerial.begin(9600);
  Serial.println("GPS инициализирован");
}
while (gpsSerial.available() > 0) {
    gps.encode(gpsSerial.read());
  }
sh = gps.location.lat(); //запись значения широты в переменную var1
d = gps.location.lng()
