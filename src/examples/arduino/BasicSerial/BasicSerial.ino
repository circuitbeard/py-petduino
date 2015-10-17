/*
 *    BasicSerial.ino - Basic serial example the PetduinoSerial library
 *    Copyright (c) 2015 Circuitbeard
 *
 *    Permission is hereby granted, free of charge, to any person
 *    obtaining a copy of this software and associated documentation
 *    files (the "Software"), to deal in the Software without
 *    restriction, including without limitation the rights to use,
 *    copy, modify, merge, publish, distribute, sublicense, and/or sell
 *    copies of the Software, and to permit persons to whom the
 *    Software is furnished to do so, subject to the following
 *    conditions:
 *
 *    This permission notice shall be included in all copies or
 *    substantial portions of the Software.
 *
 *    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 *    EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
 *    OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 *    NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
 *    HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
 *    WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 *    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
 *    OTHER DEALINGS IN THE SOFTWARE.
 */

#include <LedControl.h>
#include <Petduino.h>

#include <CmdMessenger.h>
#include <PetduinoSerial.h>

byte img1[8]={0x3c,0x02,0x81,0xc7,0xe3,0x81,0x40,0x3c};
byte img2[8]={0x3c,0x58,0x91,0x81,0x81,0x89,0x1a,0x3c};

#define IMG1_STATE 0
#define IMG2_STATE 1

PetduinoSerial pet = PetduinoSerial();

void setup() {

  // Setup Petduino
  pet.begin(9600);

  // Set initial state
  pet.setState(IMG1_STATE);

}

void loop() {

  // Update pet
  pet.update();

  // Update display based on current state
  switch(pet.getState()){

    case IMG1_STATE:
      pet.drawImage(img1);
      pet.setNextState(IMG2_STATE, 1000);
      break;
      
    case IMG2_STATE:
      pet.drawImage(img2);
      pet.setNextState(IMG1_STATE, 1000);
      break;
      
  }

}
