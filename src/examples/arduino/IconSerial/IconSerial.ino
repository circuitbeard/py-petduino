/*
 *    IconSerial.ino - Icon serial example the PetduinoSerial library
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

#define WAIT_ANIM_FRAMES 4
byte waitAnimF[WAIT_ANIM_FRAMES][8]={
  {0x3c,0x02,0x81,0xc7,0xe3,0x81,0x40,0x3c},
  {0x3c,0x58,0x91,0x81,0x81,0x89,0x1a,0x3c}
};
unsigned long waitAnimD[WAIT_ANIM_FRAMES] = { 1501, 1501 };

byte errorIco[8]={0xc3,0xe7,0x7e,0x3c,0x3c,0x7e,0xe7,0xc3};

char *icoData;

#define WAIT_STATE 0
#define DATA_STATE 1

PetduinoSerial pet = PetduinoSerial();

void setup() {

  // Setup Petduino
  pet.begin(9600);
  
  // Hookup data callback
  pet.setOnDataCallback(onData);
  
  // Draw the default img
  pet.setState(WAIT_STATE);

}

void loop() {

  // Update pet
  pet.update();
  
  // Update display based on current state
  switch(pet.getState()){

    case WAIT_STATE:
      pet.playAnimation(waitAnimF, waitAnimD, WAIT_ANIM_FRAMES, 3);
      pet.setNextState(WAIT_STATE, 9000); // Wait for connection
      break;
      
    case DATA_STATE:
      pet.stopAnimation();
      pet.clearScreen();
      
      byte val[8];
      if (strlen(icoData) == 16 && sscanf(icoData, "%2hhx%2hhx%2hhx%2hhx%2hhx%2hhx%2hhx%2hhx", 
           &val[0],&val[1],&val[2],&val[3],&val[4],&val[5],&val[6],&val[7],&val[8]) == 8)
      {
           pet.drawImage(val);
      }
      else
      {
          pet.drawImage(errorIco);
      }
      
      pet.wait();
      break;
  }

}

void onData(char *data) {
  icoData = data;
  pet.setState(DATA_STATE);
}
