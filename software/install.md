# Installation

# 1. Install System

Download image `Debian 9 with kernel 4.4.55_3` from http://wiki.banana-pi.org/Banana_Pi_BPI-M2%2B#Raspbian

Write image to SD card
``` bash
sudo fdisk -l
# SD card is /dev/mmcblk1

unzip 2018-11-09-debian-9-stretch-mate-desktop-preview-bpi-m2p-4.4-sd-emmc.img.zip

sudo dd if=2018-11-09-debian-9-stretch-mate-desktop-preview-bpi-m2p-sd-emmc.img of=/dev/mmcblk1 bs=10MB
```
Boot Banana Pi from SD card

# 2. Bluetooth Setup

``` bash
sudo apt update
sudo apt upgrade -y
sudo apt install libdbus-1-dev libglib2.0-dev libudev-dev libical-dev libreadline-dev

wget http://www.kernel.org/pub/linux/bluetooth/bluez-5.49.tar.xz

tar -xf bluez-5.49.tar.xz && rm bluez-5.49.tar.xz

cd bluez-5.49/

./configure --prefix=/usr --mandir=/usr/share/man --sysconfdir=/etc --localstatedir=/var --enable-experimental

make -j4

sudo make install

sudo adduser pi bluetooth
```

# 3. Edit bluetooth.conf
Add the marked lines to `bluetooth.conf`

```bash 
sudo cp /etc/dbus-1/system.d/bluetooth.conf /etc/dbus-1/system.d/bluetooth.conf.bak
sudo nano /etc/dbus-1/system.d/bluetooth.conf
```

```xml
<policy user="root">
    <allow own="org.bluez"/>
    <allow send_destination="org.bluez"/>
    <allow send_interface="org.bluez.Agent1"/>
    <allow send_interface="org.bluez.MediaEndpoint1"/>
    <allow send_interface="org.bluez.MediaPlayer1"/>
    <allow send_interface="org.bluez.Profile1"/>
    <!-- add start -->
        <allow send_interface="org.bluez.AlertAgent1"/>
        <allow send_interface="org.bluez.ThermometerWatcher1"/>
        <allow send_interface="org.bluez.HeartRateWatcher1"/>
        <allow send_interface="org.bluez.CyclingSpeedWatcher1"/>
    <!-- add end -->
    <allow send_interface="org.bluez.GattCharacteristic1"/>
    <allow send_interface="org.bluez.GattDescriptor1"/>
    <allow send_interface="org.bluez.LEAdvertisement1"/>
    <allow send_interface="org.freedesktop.DBus.ObjectManager"/>
    <allow send_interface="org.freedesktop.DBus.Properties"/>
  </policy>

  <!-- add start -->
    <!-- allow users of bluetooth group to communicate -->
    <policy group="bluetooth">
        <allow send_destination="org.bluez"/>
    </policy>
  <!-- add end -->

  <policy at_console="true">
    <allow send_destination="org.bluez"/>
  </policy>
```
# 4. Reboot
```bash
sudo reboot
```
# 5. Test Bluetooth

```bash
$ rfkill list

    0: sunxi-bt: Bluetooth
        Soft blocked: no
        Hard blocked: no
    1: phy0: Wireless LAN
        Soft blocked: yes
        Hard blocked: no
    2: brcmfmac-wifi: Wireless LAN
        Soft blocked: yes
        Hard blocked: no
    4: hci0: Bluetooth
        Soft blocked: yes <--
        Hard blocked: no

$ rfkill unblock bluetooth

    0: sunxi-bt: Bluetooth
        Soft blocked: no
        Hard blocked: no
    1: phy0: Wireless LAN
        Soft blocked: yes
        Hard blocked: no
    2: brcmfmac-wifi: Wireless LAN
        Soft blocked: yes
        Hard blocked: no
    4: hci0: Bluetooth
        Soft blocked: no <--
        Hard blocked: no
```
Try pairing a device
```bash
$ bluetoothctl

> power on

> agent on

> scan on

# wait a few seconds

> scan off

> pair 00:0B:CE:04:F6:66

    Attempting to pair with 00:0B:CE:04:F6:66
    Request PIN code
    [blue1m[agent] Enter PIN code: 0000

    [CHG] Device 00:0B:CE:04:F6:66 Connected: yes
    [CHG] Device 00:0B:CE:04:F6:66 UUIDs: 00001101-0000-1000-8000-00805f9b34fb
    [CHG] Device 00:0B:CE:04:F6:66 ServicesResolved: yes
    [CHG] Device 00:0B:CE:04:F6:66 Paired: yes
    Pairing successful

> info 00:0B:CE:04:F6:66

    Device 00:0B:CE:04:F6:66 (public)
    	Name: BAmobile
    	Alias: BAmobile
    	Class: 0x00001f00
    	Paired: yes
    	Trusted: no
    	Blocked: no
    	Connected: no
    	LegacyPairing: yes
    	UUID: Serial Port               (00001101-0000-1000-8000-00805f9b34fb)

> quit
```
Try to send a packet
```bash
sudo rfcomm bind 0 00:0B:CE:04:F6:66

sudo rfcomm show /dev/rfcomm0 0
#rfcomm0: 00:0B:CE:04:F6:66 channel 1 clean

#test send
sudo python3 -c 'print("\26\01\62\65\72\6c\69\6e")' > /dev/rfcomm

#test receive
cat /dev/rfcomm0
```
# 6. Install python
```bash
sudo apt update
sudo apt upgrade -y
sudo apt autoremove

sudo apt install python3-dev python3-pip python3-matplotlib

python3 -m pip install -U pip setuptools
python3 -m pip install -U matplotlib
```

## 6.1 Install pybluez for python
```bash
sudo apt-get install bluez bluez-tools
sudo apt install libbluetooth-dev

python3 -m pip install wheel pybluez
```

## 6.2 Install tkinter frontend
``` bash
sudo apt install python3-tk
python3 -m pip install tk-tools
```

## 6.3 Install SPI support
Install https://github.com/doceme/py-spidev

``` bash
python3 -m pip install spidev
```

Warning: Doesn't work on `Debian 9 with kernel 4.4.55_3`

Workaround: use gpio bitbang instead of spi device

## 6.4 Install I2C support
```bash
sudo apt install python3-smbus
python3 -m pip install smbus
```

# 7. Fix `bluetoothd` service
Edit `dbus-org.bluez.service`
```bash
sudo nano /etc/systemd/system/dbus-org.bluez.service
```
change
> ExecStart=/usr/lib/bluetooth/bluetoothd

into
> ExecStart=/usr/lib/bluetooth/bluetoothd -C

```bash
sudo systemctl daemon-reload
sudo sdptool add SP
```

# 8. Run Python serial examples

```bash
python3 tests/btSend.py

sudo hciconfig hci0 piscan

python3 tests/btRecv.py
```

# 9. Build and run Frontend

```bash
./run.sh
```
