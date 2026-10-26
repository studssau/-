#include "gps.h"
#include <TinyGPS++.h>
#include <SoftwareSerial.h>

static TinyGPSPlus gps;
static SoftwareSerial gpsSerial(4, 3);

void initGps() {
  gpsSerial.begin(9600);
  Serial.println("GPS инициализирован");
}
void readGps( float &sh, float &d) {
  while (gpsSerial.available() > 0) {
    gps.encode(gpsSerial.read());
    }
  
sh = gps.location.lat();
d = gps.location.lng();
}
