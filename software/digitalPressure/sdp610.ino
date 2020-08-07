       #include <Wire.h>
int16_t okunan;
byte crc;
float get_dp;
void setup() {
  Wire.begin(); // wake up I2C bus
  Serial.begin(9600);
  // this section will run only one time.
//  Wire.beginTransmission(0x38);
//  Wire.write(0xFA); //adress change command
//  Wire.write(0x2C); //register adress msb
//  Wire.write(0x20); // register adress lsb
//  Wire.write(0x01);   //new adress msb (new adress will be 0x21,if you want, you can change this value )
//  Wire.write(0x1F);  //new adress lsb (first six bit must 000000 and after 7 bit changeable (desired adress) last 3 bit must be 111
//                    //= result 0b0000000100001111=0x21 and final first byte(msb)=0x01 second byte (lsb) =0x0F
//  Wire.endTransmission();// sensor adress still 0x40. but after reset it will be 0x21. press arduino reset button to hard reset :)
}

void loop() {
//After change adress of sensor you can delete setup section of adress change commands
  Wire.beginTransmission(0x21); //
  Wire.write(0xF1); //
  Wire.endTransmission(); // "Thanks, goodbye..."

  Wire.requestFrom(0x21, 3); // request to from 0x21 sensor 3 byte data
  okunan = (Wire.read() << 8) | Wire.read();
  crc = Wire.read(); // crc reading but not control for error correction :)
  get_dp = okunan / 240; // look sdp610-125 datasheet
  Serial.print("Sensor1: ");
  Serial.print(okunan);
  Serial.print("----");
  Serial.println(get_dp);
  delay(100);
//---------------------------------------------------------------------------
    Wire.beginTransmission(0x41); //
  Wire.write(0xF1); //
  Wire.endTransmission(); // "Thanks, goodbye..."

    Wire.requestFrom(0x41, 3); // request to from 0x21 sensor 3 byte data
  okunan = (Wire.read() << 8) | Wire.read();
  crc = Wire.read(); // crc reading but not control for error correction :)
  get_dp = okunan / 240; // look sdp610-125 datasheet
  Serial.print("Sensor2: ");
  Serial.print(okunan);
  Serial.print("----");
  Serial.println(get_dp);
  delay(100);

  //---------------------------------------------------------------------------
      Wire.beginTransmission(0x61); //
  Wire.write(0xF1); //
  Wire.endTransmission(); // "Thanks, goodbye..."

    Wire.requestFrom(0x61, 3); // request to from 0x21 sensor 3 byte data
  okunan = (Wire.read() << 8) | Wire.read();
  crc = Wire.read(); // crc reading but not control for error correction :)
  get_dp = okunan / 240; // look sdp610-125 datasheet
  Serial.print("Sensor3: ");
  Serial.print(okunan);
  Serial.print("----");
  Serial.println(get_dp);
  delay(100);

  //---------------------------------------------------------------------------
    Wire.beginTransmission(0x31); //
  Wire.write(0xF1); //
  Wire.endTransmission(); // "Thanks, goodbye..."

    Wire.requestFrom(0x31, 3); // request to from 0x21 sensor 3 byte data
  okunan = (Wire.read() << 8) | Wire.read();
  crc = Wire.read(); // crc reading but not control for error correction :)
  get_dp = okunan / 240; // look sdp610-125 datasheet
  Serial.print("Sensor4: ");
  Serial.print(okunan);
  Serial.print("----");
  Serial.println(get_dp);
  delay(100);

  //---------------------------------------------------------------------------
    Wire.beginTransmission(0x39); //
  Wire.write(0xF1); //
  Wire.endTransmission(); // "Thanks, goodbye..."

    Wire.requestFrom(0x39, 3); // request to from 0x21 sensor 3 byte data
  okunan = (Wire.read() << 8) | Wire.read();
  crc = Wire.read(); // crc reading but not control for error correction :)
  get_dp = okunan / 240; // look sdp610-125 datasheet
  Serial.print("Sensor5: ");
  Serial.print(okunan);
  Serial.print("----");
  Serial.println(get_dp);
  delay(100);
  
    //---------------------------------------------------------------------------
    Wire.beginTransmission(0x29); //
  Wire.write(0xF1); //
  Wire.endTransmission(); // "Thanks, goodbye..."

    Wire.requestFrom(0x29, 3); // request to from 0x21 sensor 3 byte data
  okunan = (Wire.read() << 8) | Wire.read();
  crc = Wire.read(); // crc reading but not control for error correction :)
  get_dp = okunan / 240; // look sdp610-125 datasheet
  Serial.print("Sensor6: ");
  Serial.print(okunan);
  Serial.print("----");
  Serial.println(get_dp);
  delay(100);

    //---------------------------------------------------------------------------
    Wire.beginTransmission(0x35); //
  Wire.write(0xF1); //
  Wire.endTransmission(); // "Thanks, goodbye..."

    Wire.requestFrom(0x35, 3); // request to from 0x21 sensor 3 byte data
  okunan = (Wire.read() << 8) | Wire.read();
  crc = Wire.read(); // crc reading but not control for error correction :)
  get_dp = okunan / 240; // look sdp610-125 datasheet
  Serial.print("Sensor7: ");
  Serial.print(okunan);
  Serial.print("----");
  Serial.println(get_dp);
  delay(100);

    //---------------------------------------------------------------------------
    Wire.beginTransmission(0x40); //
  Wire.write(0xF1); //
  Wire.endTransmission(); // "Thanks, goodbye..."

    Wire.requestFrom(0x40, 3); // request to from 0x21 sensor 3 byte data
  okunan = (Wire.read() << 8) | Wire.read();
  crc = Wire.read(); // crc reading but not control for error correction :)
  get_dp = okunan / 240; // look sdp610-125 datasheet
  Serial.print("Sensor8: ");
  Serial.print(okunan);
  Serial.print("----");
  Serial.println(get_dp);
  delay(1000);
}
