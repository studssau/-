#ifndef GPS_H
#define GPS_H
#include <Arduino.h>
void initGps(); // для инициализации GPS-модуля
void readGps(float &sh, float &d); // для чтения показаний
#endif
