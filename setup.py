#!/usr/bin/env python

import os, sys, glob, shutil
from distutils.core import setup, Extension

#if sys.platform.startswith ("win"):
#    import py2exe

VERSION = open ("VERSION").readline ().strip ()

def RemoveDir (d):
    for root, dirs, files in os.walk (d, topdown=False):
        for name in files:
            os.remove (os.path.join (root, name))
        for name in dirs:
            os.rmdir (os.path.join (root, name))
    os.rmdir (d)

op = None
for x in sys.argv [1:]:
    if x == "clean" or x == "install" or x == "build":
        op = x

# Create mo files:
mofiles = []
for pofile in glob.glob('po/*.po'):
    lang = os.path.splitext (os.path.basename (pofile)) [0]
    # Piggyback on the lib/ directory used by setup()
    path = "build/locale/" + lang
    if not os.path.exists(path):
        os.makedirs (path, 0755)
    mofile = path + "/xpd.mo"
    if op == "install" or op == "build":
        print "Generating", mofile
        os.system("msgfmt %s -o %s" % (pofile, mofile))
    mofiles.append (('share/locale/' + lang + '/LC_MESSAGES', [mofile]))

# Patch module version in __init__.py
ct = open ("xpdm/__init__.py").readlines ()
for ln in range (0, len (ct)):
    if ct [ln].find ("VERSION =") >= 0:
        ct [ln] = "VERSION = \"%s\"\n" % VERSION
open ("xpdm/__init__.py", "w").writelines (ct)

# Also patch the spec file
ct = open ("build/xpd.spec").readlines ()
for ln in range (0, len (ct)):
    if ct [ln].find ("Version:") >= 0:
        ct [ln] = "Version:        %s\n" % VERSION
open ("build/xpd.spec", "w").writelines (ct)

setup (name = 'xpd',
        version = VERSION,
        description = 'A tool for setting up Infineon-based e-bike controllers',
        author = 'Andrey Zabolotnyi',
        author_email = 'zap@cobra.ru',
        url = 'http://xpd.berlios.de/',
        license = 'GPL',
        platforms = ['Unix'],
        classifiers = [
            'Development Status :: 3 - Alpha',
            'Environment :: X11 Applications',
            'Environment :: Win32 (MS Windows)',
            'Intended Audience :: End Users/Desktop',
            'License :: GNU General Public License (GPL)',
            'Operating System :: Linux',
            'Operating System :: Microsoft :: Windows',
            'Programming Language :: Python',
            'Topic :: System :: Hardware :: Hardware Drivers',
            ],
        packages = ["xpdm"],
        package_dir = { "xpdm": "xpdm" },
        scripts = ['xpd'],
        data_files = [
            ('share/xpd', ['share/gui.xml', 'share/xpd.svg'] + glob.glob ('share/*.asv')),
            ('share/applications', ['build/xpd.desktop']),
            ('share/pixmaps', ['share/xpd.svg'])
            ] + mofiles,
        long_description = """
This program was developed to be a drop-in cross-platform replacement
for the widely known in close circles Parameter Design tool (also known
as Keywin e-Bike Lab), used to set the parameters of a e-bike controller
based on the Infineon XC846 microcontroller (and various clones).""",
        windows = [ {"script" : "xpd"} ],
        )

if op == "clean":
    RemoveDir ("build/locale")
