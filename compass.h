#ifndef COMPASS_H
#define COMPASS_H
#include <Arduino.h>
void initCompass(); // для инициализации магнитометра
void readCompass(int &x, int &y, int &z ); // для чтения показаний
#endif
