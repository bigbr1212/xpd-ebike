# What is this? #

XPD is a cross-platform, open-source rewrite of a tool named Parameter Designer (sometimes also named Keywin e-Bike Lab) (in the following I will use the abbreviation KWEBL). The original program was written in Visual Basic, and only the windows executable file was distributed, thus, it is not possible to enhance or port it to other platforms.

I started this project after I discovered how easy was to understand the serial protocol used between the Parameter Designer and the e-bike controller. Besides, I had a dream to be able to change e-bike settings anytime, anywhere. This would be possible if it would be possible to change controller settings using some portable device with serial port capabilities, for example my Nokia N900 phone.

The obligatory screenshot:

![https://xpd-ebike.googlecode.com/svn/trunk/docs/img/screenshot.png](https://xpd-ebike.googlecode.com/svn/trunk/docs/img/screenshot.png)

# Differences between XPD and its predcessor #

You may notice several differences between the way how XPD presents the controller parameters, and the way how Parameter Designer used to do it. I'll list here the most important differences, with detailed explanations.

  * Q: Many numeric parameters have 0.1 precision, while KWEBL uses integer numbers.
  * A: Of course, nobody should expect the controller will control these values up to the displayed precision. However, controller uses different units internally for most values, and if you translate successive internal-units values to SI system using integer values, you might get the same number for different amounts in internal controller units. Thus I have decided to display the values with 0.1 precision, this will let you choose between 31.9 and 32.2 amperes (which otherwise would be both displayed as 32).

  * Q: 121% speed? WTF? Why not 120%?
  * A: As said above, controller uses different units for most parameters, and they are integer numbers in the range 0-255. For example, controller value 90 maps to 114.3% speed, 91 to 115.6%, 92 to 116.8%, 93 to 118.1%, 94 to 119.4% and 95 to 120.7%. When these numbers are rounded to nearest integer, 120.7 is rounded to 121%, and 119.4 is rounded to 119%. That's why there's no "120%" setting at all.

  * Q: The range of selectable values is SO MUCH larger
  * A: As I said before, the controller uses its internal scale for measuring volts and amperes. This scale depends on the values of some components on the board, and for some controllers the internal range would really map to this extremely large real-world scale. This does not really mean that EB218 will handle phase currents up to 1300 amperes (wow) in the real world, you still have to make sure the actual power MOSFETs can deal properly with the selected currents.

  * Q: Why KWEBL can't load asv files saved by XPD?
  * A: There are several variants of Parameter Designer, and one can't even load the files saved by another variant. The reason is that the asv format is utterly broken, XPD accepted it just for the reason not to create yet another parameter format, but this may change in the future, if PD authors will keep changing it with every release. The ugly thing is the way how Parameter Designer loads asv files: it matches not only the numeric values, but the textual hints (which come after a ':') as well; this means incompatibility between English, Chinese, French, Lyen versions of Parameter Designer. XPD has chosen to save just the numeric values, without the double-colon and textual hint after them.

# License #

XPD is licensed under the terms of [GNU General Public License](http://www.gnu.org/licenses/gpl.html) version 3 or later.

# Credits #

I would like to thank:

  * Maximilian Federle <max.federle@googlemail.com> for the German translation of the program.
  * The BerliOS project for hosting all my small
public projects for many years for free. Unfortunately, BerliOS project was closed so I moved here.