
## Modifying UI with PyQt5 designer

on Ubuntu / Debian

``` bash
sudo apt install qt4-designer
designer-qt4
```

Location of PyQt5 designer.exe on Windows
> C:\Program Files\Python36\Lib\site-packages\pyqt5-tools\

or

> C:\Users\\\<User>\AppData\Local\Programs\Python\\\<version>\Lib\site-packages\pyqt5-tools\

## Regenerate UI

on Linux

```bash
python3 -m PyQt5.uic.pyuic youruifile -o yourpyfile -x
```

on Windows

```cmd
pyuic5 youruifile -o yourpyfile -x
```

## Running

```bash
cd software/
python3 main.py
```
