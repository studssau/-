#include "compass.h"
#include <Wire.h>
#include <QMC5883LCompass.h>
static QMC5883LCompass compass;
void initCompass() {
  compass.init();
  Serial.println("Компас инициализирован");
}
void readCompass(int &x, int &y, int &z ) {
 compass.read();
  x = compass.getX();
    y = compass.getY();
      z = compass.getZ();
} 
