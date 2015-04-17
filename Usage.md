# Usage #

The basic usage of the program should be quite obvious for anybody who can handle a computer mouse. The main program window displays a list of existing controller profiles, you may create, edit, delete and apply profiles. In the bottom-right corner of the window you may select the serial port to which you connected the controller programming cable.

The controller looks for profiles in two directories: first, this is the program data directory (`/usr/share/xpd/` on Linux, `share/` on Windows), and second, in the user's home data directory (`~/.local/share/xpd/` on Linux, `C:\Documents and Settings\Username\My Documents\xpd` on Windows).

Also on Linux I would suggest to enable icons-on-buttons (which is now disabled by default in GNOME, and the interface settings page was removed too, [it was argued](http://mail.gnome.org/archives/gnomecc-list/2009-July/msg00015.html) that icons on buttons are "bad design decisions"). So you'll have to launch gconf-editor, navigate to `/desktop/gnome/interface/` folder and enable the `buttons_have_icons` setting.

# Problems and solutions #

## Linux ##

It may happen that the "Serial port" combobox in xpd is empty. This means one of two things: either you don't have serial ports at all, or your user account does not have access to serial port devices. Check the access rights on the serial ports:

```
$ ls -la /dev/tty*S*
crw-rw---- 1 root dialout   4, 64 Июн  4 23:55 /dev/ttyS0
crw-rw---- 1 root dialout   4, 65 Май 11 21:00 /dev/ttyS1
crw-rw---- 1 root dialout   4, 66 Май 11 21:00 /dev/ttyS2
crw-rw---- 1 root dialout   4, 67 Май 11 21:00 /dev/ttyS3
crw-rw---- 1 root dialout 188,  0 Июн  5 10:07 /dev/ttyUSB0
crw-rw---- 1 root dialout 188,  1 Июн  5 10:07 /dev/ttyUSB1
```

Okay, so the "dialout" group has write access to serial ports. Now you just have
to add your account to this group ("dialout" in my case), either via administration
tools, or quicker via the command line:

`$ usermod -a -G dialout <userid>`

Now relogon, and you should gain access to serial ports.

Another problem that may happen is that some shitty tools may put various trash
into the serial ports at random times. For example, openct contains a driver for
smart card readers attached to serial ports (`/lib/udev/openct_serial`).
To simulate "plug-and-pray" this shit often writes to serial port various strings,
waiting for an answer from the device. If you get unexpected problems (e.g. xpd
starts talking with the controller then locks, etc), you may try to catch the
S-O-B with the pants down by using the command:

`fuser -v /dev/ttyUSB0 # or whatever serial port you are using`

This command will list the processes that use a file (or device). I recommend deinstalling the openct package, most people don't need it anyway.