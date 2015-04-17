# Microsoft Windows #

First, download [the support files](https://drive.google.com/folderview?id=0B09H_OVSYJ1tbW1XNlhleWNvVEk&usp=sharing) from this directory to some temporary directory (the files may be deleted after they are used). There are three installers for three XPD pre-requisites:
  * `python-2.7.1.msi` - This is the interpreter for the Python programming language, install it first.
  * `pygtk-all-in-one-2.22.6.win32-py2.7.msi` - This is the GTK+ llibrary (the graphical user interface library) and the Python bindings for it, install this after Python.
  * `pyserial-2.5.win32.exe` - Run this to install the PySerial library

Now download [XPD itself](https://drive.google.com/folderview?id=0B09H_OVSYJ1tZG04VlR6WHNlMFU&usp=sharing), `xpd-*-windows.zip` from the subdirectory with the latest version, and unzip it to `C:\Program Files\`
(or any other place at your choice).

Open the `xpd-*` folder (created when you extract the archive), you will see two icons: the XPD program and the XPD icon. Run the program (not the icon :)) with a double-click. If all goes well, it should start and you will see a window with a list of pre-defined controller profiles.

If you intend to use it often, create a shortcut for it (Ctrl+Shift and drag the program to desktop), then you may change program's icon to the one provided in xpd directory.

Also, of course, you must install the drivers for the respective USB-to-UART cable you are using (PL2303, FT232, CP2102 etc).

# Linux #

If you're using the Ubuntu/Debian or Fedora Linux distributions, just download [the respective binary package](https://drive.google.com/folderview?id=0B09H_OVSYJ1tZG04VlR6WHNlMFU&usp=sharing) (.deb or .rpm respectively) from the subdirectory with latest version number and install it.

Otherwise, download [the source code tarball](https://drive.google.com/folderview?id=0B09H_OVSYJ1tZG04VlR6WHNlMFU&usp=sharing) (`xpd-*.tar.bz2`), unpack it somewhere, enter the `xpd-*` directory and run "make install" as root. If all pre-requisites are in place (e.g. Python, PySerial, PyGTK) it will easily install. Now you can run xpd
either via the "Applications" menu (should be in "Electronics" section), or just run the "xpd" command from terminal or otherwise.