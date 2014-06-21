# -*- coding: utf-8 -*-
# Basic Infineon-style e-bike controller class
#

import os
import gtk
import ctypes
import math
from xpdm import FNENC

# Parameter widget types for editing
PWT_COMBOBOX = 0
PWT_SPINBUTTON = 1

# A list of controller families
Families = []


def RegisterFamily (Family, Profile, Models, DetectFormat):
    Families.append ([Family, Profile, Models, DetectFormat])


class Profile:
    Family = None
    FileName = None
    Description = None

    # Parameter order when loading from .asv files
    ParamLoadOrder = []

    # The order of parameters in the profile edit dialog
    ParamEditOrder = []

    # The order of parameters in raw binary data sent to controller
    ParamRawOrder = []


    def __init__ (self, Family, FileName, ControllerTypeDesc, ControllerParameters):
        self.ControllerTypeDesc = ControllerTypeDesc
        self.ControllerParameters = ControllerParameters
        self.SetFileName (FileName)
        self.Family = Family
        for parm, desc in self.ControllerParameters.items ():
            setattr (self, parm, desc ["Default"])


    def SetFileName (self, fn, rename = True):
        self.Description = os.path.splitext (os.path.basename (fn)) [0]

        fn = fn.encode (FNENC)

        if rename:
            # If file with old name exists, rename it
            if (self.FileName != None) and os.access (self.FileName, os.R_OK):
                os.rename (self.FileName, fn)

        self.FileName = fn


    def SetDescription (self, desc):
        self.SetFileName (os.path.join (
            os.path.dirname (self.FileName).decode (FNENC), desc + ".asv"))


    def Load (self, fn, lines):
        vi = 0
        for l in lines:
            # Remove extra shit from the string
            l = l.strip ()
            try:
                l = l [:l.index (":")]
            except ValueError:
                pass

            if vi >= len (self.ControllerParameters):
                if len (l):
                    raise ValueError, \
                        _("Extra data at the end of file:\n'%(data)s'") % \
                        { "data" : l }
            else:
                parm = self.ParamLoadOrder [vi]
                desc = self.ControllerParameters [parm]
                if desc ["Type"].find ('i') >= 0:
                    setattr (self, parm, int (l))
                elif desc ["Type"].find ('f') >= 0:
                    setattr (self, parm, float (l))

            vi = vi + 1


    def Save (self):
        lines = []
        for parm in self.ParamLoadOrder:
            desc = self.ControllerParameters [parm]
            if desc ["Type"].find ('i') >= 0:
                # Hack for controller type
                if desc ["Type"].find ('/') >= 0:
                    model = self.GetModel ()
                    if model.find ('/') >= 0:
                        model = model [:model.find ('/')]
                    lines.append ("%d:%s" % (getattr (self, parm), model))
                else:
                    lines.append ("%d" % getattr (self, parm))
            elif desc ["Type"].find ('f') >= 0:
                mask = "%%.%df" % desc.get ("Precision", 1)
                lines.append (mask % getattr (self, parm))

            # Append a CR since the file uses windows line endings
            lines [-1] += '\r'

        f = open (self.FileName, "wb")
        f.write ('\n'.join (lines) + '\n')
        f.close ()


    def GetController (self):
        if (self.ControllerType > 0) and (self.ControllerType <= len (self.ControllerTypeDesc)):
            return self.ControllerTypeDesc [self.ControllerType - 1]

        return self.ControllerTypeDesc [0]


    def GetModel (self):
        if (self.ControllerType > 0) and (self.ControllerType <= len (self.ControllerTypeDesc)):
            return self.ControllerTypeDesc [self.ControllerType - 1]["Name"]

        return "???"


    def Remove (self):
        if self.FileName:
            os.remove (self.FileName)


    def FillParameters (self, vbox):
        rowcidx = 0
        rowcolors = [ gtk.gdk.Color (1.0, 1.0, 1.0), gtk.gdk.Color (1.0, 0.94, 0.86) ]

        self.EditWidgets = {}

        for parm in self.ParamEditOrder:
            if type (parm) == list:
                expd = gtk.Expander (parm [0])
                expd.set_expanded (True)
                expd.set_border_width (1)
                expd.set_spacing (3)
                expd_vbox = gtk.VBox (False, 1)
                expd.add (expd_vbox)
                vbox.pack_start (expd, False, True, 0)
                continue

            desc = self.ControllerParameters [parm]

            # Place the hbox in a event box to be able to change background color
            evbox = gtk.EventBox ()
            hbox = gtk.HBox (False, 5)
            hbox.set_border_width (2)
            evbox.add (hbox)
            evbox.set_tooltip_text (desc ["Description"])
            expd_vbox.pack_start (evbox, False, True, 0)

            label = gtk.Label (desc ["Name"])
            label.set_alignment (0.0, 0.5)

            evbox.modify_bg (gtk.STATE_NORMAL, rowcolors [rowcidx])
            rowcidx ^= 1
            hbox.pack_start (label, True, True, 0)

            if desc ["Widget"] == PWT_COMBOBOX:
                minv, maxv = desc ["Range"]
                cb = gtk.combo_box_new_text ()
                for i in range (minv, maxv + 1):
                    cb.append_text (desc ["GetDisplay"] (self, i))
                cb.set_active (getattr (self, parm) - minv)
                hbox.pack_start (cb, False, True, 0)
                cb.connect ("changed", self.ComboBoxChangeValue, parm, desc)
                self.EditWidgets [parm] = cb

            elif desc ["Widget"] == PWT_SPINBUTTON:
                minv, maxv = desc ["Range"]
                spin = gtk.SpinButton (climb_rate = 1.0)
                try:
                    val = desc ["SetDisplay"] (self, getattr (self, parm))
                except IndexError:
                    val = desc ["Default"]
                spin.get_adjustment ().configure (val, minv, maxv, 1, 5, 0)
                spin.set_width_chars (7)
                hbox.pack_start (spin, False, True, 0)
                spin.connect ("output", self.SpinButtonOutput, parm, desc)
                spin.connect ("input", self.SpinButtonInput, parm, desc)
                spin.connect ("value-changed", self.SpinButtonValueChanged, parm, desc)
                self.EditWidgets [parm] = spin

        vbox.show_all ()


    def ComboBoxChangeValue (self, cb, parm, desc):
        minv, maxv = desc ["Range"]
        setattr (self, parm, minv + cb.get_active ())
        # Check if any depending controls needs updating
        for iparm, idesc in self.ControllerParameters.items ():
            if idesc.has_key ("Depends"):
                if parm in idesc ["Depends"]:
                    self.EditWidgets [iparm].update ()


    def SpinButtonOutput (self, spin, parm, desc):
        desc = self.ControllerParameters [parm]
        if desc.get ("Units") is None:
            mask = "%%.%df" % desc.get ("Precision", 1)
        else:
            mask = "%%.%df %s" % (desc.get ("Precision", 1), desc.get ("Units", "").replace ('%', '%%'))
        spin.set_text (mask % desc ["GetDisplay"] (self, spin.props.adjustment.value))
        return True


    # gptr hack, see http://www.mail-archive.com/pygtk@daa.com.au/msg16384.html
    def SpinButtonInput (self, spin, gptr, parm, desc):
        text = spin.get_text ().strip ()
        if desc.has_key ("Units"):
            try:
                text = text [:text.rindex (desc ["Units"])]
            except ValueError:
                pass
        try:
            val = float (desc ["SetDisplay"] (self, float (text.strip ())))
        except ValueError:
            val = spin.props.adjustment.value

        double = ctypes.c_double.from_address (hash (gptr))
        double.value = val
        return True


    # don't allow the displayed value to go below zero
    def SpinButtonValueChanged (self, spin, parm, desc):
        while desc ["GetDisplay"] (self, spin.props.adjustment.value) < 0:
            spin.props.adjustment.value += 1
        val = desc ["GetDisplay"] (self, spin.props.adjustment.value)
        prec = desc.get ("Precision", 1)
        val = round (val * math.pow (10, prec)) / math.pow (10, prec)
        setattr (self, parm, val)


    def BuildRaw (self):
        data = bytearray ()

        for x in self.ParamRawOrder:
            if type (x) == str:
                if self.ControllerParameters [x].has_key ("ToRaw"):
                    x = self.ControllerParameters [x]["ToRaw"] (self, getattr (self, x))
                elif self.ControllerParameters [x]["Widget"] == PWT_COMBOBOX:
                    x = round (getattr (self, x))
                elif self.ControllerParameters [x]["Widget"] == PWT_SPINBUTTON:
                    x = self.ControllerParameters [x]["SetDisplay"] (self, getattr (self, x))

            data.append (int (x))

        # temporary hack until someone finds out what means the 23th byte
        if "Byte23" in self.ControllerTypeDesc [self.ControllerType - 1]:
            data [23] = self.ControllerTypeDesc [self.ControllerType - 1]["Byte23"]

        crc = 0
        for x in data:
            crc = crc ^ x
        data.append (crc)

        return data


    def CopyParameters (self, other):
        for parm in self.ControllerParameters.keys ():
            if hasattr (other, parm):
                setattr (self, parm, getattr (other, parm))
