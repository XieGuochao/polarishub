## ReadMe for Python Library

##### Written by TPIOS

This is a p2p file transfer program via LAN.

This program is implemented with Django Framework. External libraries required: MyQR for generating QR code.

To run the library correctly, you should first create a Python script file to setup polarishub on your computer. In this Python script file, only two lines will be include.

```python
from polarishub import setup
setup.initialization()
```

Then run this script file to setup the essential environment for polarishub.



To run the polarishub on your computer, you should write another Python script file:

```python
from polarishub import manage
manage.runserver(ipAddress, port)
# here ipAddress and port are default as "0.0.0.0" and "8000"
# if you want to change them, you should use your own address and port.
```