# -*- coding: utf-8 -*-
# Infineon-style e-bike controller profile
#

import serial
import time
import locale
from xpdm import infineon

# -- # Constants # -- #

# Motor sensor angle
SA_120 = 0
SA_60 = 1
SA_COMPAT = 2

SensorAngleDesc = [ "120°", "60°", _("Auto") ]

# Three-speed switch modes
SSM_SWITCH = 0
SSM_CYCLE3 = 1
SSM_HISWITCH = 2
SSM_CYCLE4 = 3

SpeedSwitchModeDesc = [ _("Switch"), _("Cycle 3"), _("High Switch"), _("Cycle 4") ]

# LED indicator mode
IM_COMM_VCC = 0
IM_COMM_GND = 1

IndicatorModeDesc = [ _("Common VCC"), _("Common GND") ]

# Slip charge mode
SCM_ENABLE = 0
SCM_DISABLE = 1

SlipChargeModeDesc = [ _("Enable"), _("Disable") ]

# EBS level
EBS_DISABLED = 0
EBS_MODERATE = 1
EBS_STRONG = 2

EBSLevelDesc = [ _("Disabled"), _("Moderate"), _("Strong"), _("Unlimited") ]
EBSLevel2Raw = [ 0, 4, 8, 255 ]

# Guard mode signal polarity (anti-theft)
GP_LOW = 0
GP_HIGH = 1

GuardLevelDesc = [ _("Low"), _("High") ]

# Throttle blowout protect
TBP_DISABLE = 0
TBP_ENABLE = 1

ThrottleProtectDesc = [ _("Disabled"), _("Enabled") ]

# Pedal Assisted Sensor mode
PAS_FAST = 0
PAS_SLOW = 1

PASModeDesc = [ _("Fast"), _("Slow") ]

# Cruise limit
CruiseLimitDesc = [ _("No"), _("Yes") ]

# Default speed
DefaultSpeedDesc = [ _("Speed 1"), _("Speed 2"), _("Speed 3"), _("Speed 4") ]

# Controller type descriptions
ControllerTypeDesc = \
[
    {
        "Name"             : "EB306",
        "PhaseCurrent2Raw" : lambda I: (I * 1.25) - 0.2,
        "Raw2PhaseCurrent" : lambda R: 0.16 + (0.8 * R),
        "BattCurrent2Raw"  : lambda I: (I * 1.4) + 0.15,
        "Raw2BattCurrent"  : lambda R: (0.71 * R) - 0.1,
        "Voltage2Raw"      : lambda U: U * 3.184,
        "Raw2Voltage"      : lambda R: R / 3.184,
    },
    {
        "Name"             : "EB309",
        "PhaseCurrent2Raw" : lambda I: (I * 1.25) - 10.2,
        "Raw2PhaseCurrent" : lambda R: 8.16 + (0.8 * R),
        "BattCurrent2Raw"  : lambda I: (I * 1.4) + 0.15,
        "Raw2BattCurrent"  : lambda R: (0.71 * R) - 0.1,
        "Voltage2Raw"      : lambda U: U * 3.184,
        "Raw2Voltage"      : lambda R: R / 3.184,
    },
    {
        "Name"             : "EB312",
        "PhaseCurrent2Raw" : lambda I: (I * 0.624) - 6,
        "Raw2PhaseCurrent" : lambda R: 9.6 + (1.6 * R),
        "BattCurrent2Raw"  : lambda I: (I * 0.7) + 0.07,
        "Raw2BattCurrent"  : lambda R: (1.43 * R) - 0.1,
        "Voltage2Raw"      : lambda U: U * 3.184,
        "Raw2Voltage"      : lambda R: R / 3.184,
    },
    {
        "Name"             : "EB315",
        "PhaseCurrent2Raw" : lambda I: I * 0.624 - 12,
        "Raw2PhaseCurrent" : lambda R: 19.2 + (1.6 * R),
        "BattCurrent2Raw"  : lambda I: (I * 0.7) + 0.07,
        "Raw2BattCurrent"  : lambda R: (1.43 * R) - 0.1,
        "Voltage2Raw"      : lambda U: U * 3.184,
        "Raw2Voltage"      : lambda R: R / 3.184,
    },
    {
        "Name"             : "EB318",
        "PhaseCurrent2Raw" : lambda I: I * 0.416 - 11.9,
        "Raw2PhaseCurrent" : lambda R: 28.6 + (2.4 * R),
        "BattCurrent2Raw"  : lambda I: (I * 0.467) + 0.03,
        "Raw2BattCurrent"  : lambda R: (2.14 * R) - 0.06,
        "Voltage2Raw"      : lambda U: U * 3.184,
        "Raw2Voltage"      : lambda R: R / 3.184,
    },
    {
        "Name"             : "EB306/CellMan",
        "PhaseCurrent2Raw" : lambda I: (I * 0.624) - 6,
        "Raw2PhaseCurrent" : lambda R: 9.6 + (1.6 * R),
        "BattCurrent2Raw"  : lambda I: (I * 0.7) + 0.07,
        "Raw2BattCurrent"  : lambda R: (1.43 * R) - 0.1,
        "Voltage2Raw"      : lambda U: U * 3.184,
        "Raw2Voltage"      : lambda R: R / 3.184,
    },
    {
        "Name"             : "EB309/CellMan",
        "PhaseCurrent2Raw" : lambda I: (I * 0.624) - 6,
        "Raw2PhaseCurrent" : lambda R: 9.6 + (1.6 * R),
        "BattCurrent2Raw"  : lambda I: (I * 0.7) + 0.07,
        "Raw2BattCurrent"  : lambda R: (1.43 * R) - 0.1,
        "Voltage2Raw"      : lambda U: U * 3.184,
        "Raw2Voltage"      : lambda R: R / 3.184,
    },
    {
        "Name"             : "EB312/CellMan",
        "PhaseCurrent2Raw" : lambda I: (I * 0.312) - 3,
        "Raw2PhaseCurrent" : lambda R: 9.6 + (3.2 * R),
        "BattCurrent2Raw"  : lambda I: (I * 0.35) + 0.035,
        "Raw2BattCurrent"  : lambda R: (2.86 * R) - 0.1,
        "Voltage2Raw"      : lambda U: U * 3.184,
        "Raw2Voltage"      : lambda R: R / 3.184,
    },
    {
        "Name"             : "EB318/CellMan",
        "PhaseCurrent2Raw" : lambda I: (I * 0.208) - 5.95,
        "Raw2PhaseCurrent" : lambda R: 28.6 + (4.8 * R),
        "BattCurrent2Raw"  : lambda I: (I * 0.2335) + 0.015,
        "Raw2BattCurrent"  : lambda R: (4.28 * R) - 0.06,
        "Voltage2Raw"      : lambda U: U * 3.184,
        "Raw2Voltage"      : lambda R: R / 3.184,
    },
];


# This array describes all the controller parameters
ControllerParameters = \
{
    "ControllerType" :
    {
        "Type"        : "i/",
        "Name"        : _("Controller type"),
        "Description" : _("""\
The type of your controller. This influences the coefficients assumed for \
various parts of the controller, e.g. shunts, resistive dividers. If you \
have a non-standard controller, you may create your own type in infineon.py\
"""),
        "Default"     : 1,
        "Widget"      : infineon.PWT_COMBOBOX,
        "Range"       : (1, len (ControllerTypeDesc)),
        "GetDisplay"  : lambda prof, v: ControllerTypeDesc [v - 1]["Name"],
    },

    "PhaseCurrent" :
    {
        "Type"        : "f",
        "Name"        : _("Phase current limit"),
        "Description" : _("""\
The current limit in motor phase wires. Since the e-bike controller is, \
in a sense, a step-down DC-DC converter, the motor current can actually be \
much higher than the battery current. When setting this parameter, make \
sure you don't exceed the capabilities of the MOSFETs in your controller. \
This parameter mostly affects the acceleration on low speeds.\
"""),
        "Default"     : 30,
        "Depends"     : [ "ControllerType" ],
        "Units"       : _("A"),
        "Widget"      : infineon.PWT_SPINBUTTON,
        "Range"       : (1, 255),
        "GetDisplay"  : lambda prof, v: prof.GetController () ["Raw2PhaseCurrent"] (v),
        "SetDisplay"  : lambda prof, v: round (prof.GetController () ["PhaseCurrent2Raw"] (v)),
    },

    "BatteryCurrent" :
    {
        "Type"        : "f",
        "Name"        : _("Battery current limit"),
        "Description" : _("""\
The limit for the current drawn out of the battery. Make sure this does \
not exceed the specs for your battery, otherwise you will lose a lot of \
energy heating up the battery (and may blow it, too).\
"""),
        "Default"     : 14,
        "Depends"     : [ "ControllerType" ],
        "Units"       : _("A"),
        "Widget"      : infineon.PWT_SPINBUTTON,
        "Range"       : (1, 255),
        "GetDisplay"  : lambda prof, v: prof.GetController () ["Raw2BattCurrent"] (v),
        "SetDisplay"  : lambda prof, v: round (prof.GetController () ["BattCurrent2Raw"] (v)),
    },

    "HaltVoltage" :
    {
        "Type"        : "f",
        "Name"        : _("Battery low voltage"),
        "Description" : _("""\
The voltage at which controller cuts of the power. Make sure this is \
at least equal to lowest_cell_voltage x cell_count (e.g. for a \
12S LiFePO4 battery this would be 2.6 * 12 = 31.2V). This does not \
matter much if you use a BMS, since it will cut the power as soon \
as *any* cell reaches the lowest voltage, which is much better for \
the health of your battery.\
"""),
        "Default"     : 32.5,
        "Depends"     : [ "ControllerType" ],
        "Units"       : _("V"),
        "Widget"      : infineon.PWT_SPINBUTTON,
        "Range"       : (1, 255),
        "GetDisplay"  : lambda prof, v: prof.GetController () ["Raw2Voltage"] (v),
        "SetDisplay"  : lambda prof, v: round (prof.GetController () ["Voltage2Raw"] (v)),
    },

    "VoltageTolerance" :
    {
        "Type"        : "f",
        "Name"        : _("Battery low voltage threshold"),
        "Description" : _("""\
The amount of volts for the battery voltage to rise after a cutoff \
due to low voltage for the controller to restore power back. This is \
most useful for plumbum batteries, as they tend to restore voltage \
after a bit of rest.\
"""),
        "Default"     : 1.0,
        "Depends"     : [ "ControllerType" ],
        "Units"       : _("V"),
        "Widget"      : infineon.PWT_SPINBUTTON,
        "Range"       : (1, 255),
        "GetDisplay"  : lambda prof, v: prof.GetController () ["Raw2Voltage"] (v),
        "SetDisplay"  : lambda prof, v: round (prof.GetController () ["Voltage2Raw"] (v)),
    },

    "SpeedSwitchMode" :
    {
        "Type"        : "i",
        "Name"        : _("Speed switch mode"),
        "Description" : _("""\
The way how the speed switch functions. When in 'Switch' mode you may \
use a three-position switch which connects X1 (speed 1) or X2 (speed 3) \
to GND, or leaves both unconnected (speed 2). In 'Cycle 3' mode connecting \
X1 to ground with a momentary switch will cycle speeds 1-2-3. \
The 'High Switch' mode is similar to 'Switch', but X1/X2 should \
connect to high voltage (+5V or +BAT). The 'Cycle 4' mode is like \
'Cycle 3', but cycles between speeds 1-2-3-4.\
"""),
        "Default"     : SSM_SWITCH,
        "Widget"      : infineon.PWT_COMBOBOX,
        "Range"       : (0, 3),
        "GetDisplay"  : lambda prof, v: SpeedSwitchModeDesc [v],
    },

    "Speed1" :
    {
        "Type"        : "i",
        "Name"        : _("Speed 1"),
        "Description" : _("""\
The first speed limit (see comment to 'speed switch mode').\
"""),
        "Default"     : 100,
        "Units"       : "%",
        "Widget"      : infineon.PWT_SPINBUTTON,
        "Precision"   : 0,
        "Range"       : (1, 95),
        "GetDisplay"  : lambda prof, v: v * 1.26,
        "SetDisplay"  : lambda prof, v: round (v / 1.26),
    },

    "Speed2" :
    {
        "Type"        : "i",
        "Name"        : _("Speed 2"),
        "Description" : _("""\
The second speed limit (see comment to 'speed switch mode').\
"""),
        "Default"     : 100,
        "Units"       : "%",
        "Widget"      : infineon.PWT_SPINBUTTON,
        "Precision"   : 0,
        "Range"       : (1, 95),
        "GetDisplay"  : lambda prof, v: v * 1.26,
        "SetDisplay"  : lambda prof, v: round (v / 1.26),
    },

    "Speed3" :
    {
        "Type"        : "i",
        "Name"        : _("Speed 3"),
        "Description" : _("""\
The third speed limit (see comment to 'speed switch mode').\
"""),
        "Default"     : 100,
        "Units"       : "%",
        "Widget"      : infineon.PWT_SPINBUTTON,
        "Precision"   : 0,
        "Range"       : (1, 95),
        "GetDisplay"  : lambda prof, v: v * 1.26,
        "SetDisplay"  : lambda prof, v: round (v / 1.26),
    },

    "Speed4" :
    {
        "Type"        : "i",
        "Name"        : _("Speed 4"),
        "Description" : _("""\
The fourth speed limit (see comment to 'speed switch mode').\
"""),
        "Default"     : 100,
        "Units"       : "%",
        "Widget"      : infineon.PWT_SPINBUTTON,
        "Precision"   : 0,
        "Range"       : (1, 95),
        "GetDisplay"  : lambda prof, v: v * 1.26,
        "SetDisplay"  : lambda prof, v: round (v / 1.26),
    },

    "LimitedSpeed" :
    {
        "Type"        : "i",
        "Name"        : _("Limited speed"),
        "Description" : _("""\
The speed corresponding to 100% throttle when the 'speed limit' \
switch/wires are enabled (when the 'SL' board contact is connected \
to ground).\
"""),
        "Default"     : 100,
        "Units"       : "%",
        "Widget"      : infineon.PWT_SPINBUTTON,
        "Precision"   : 0,
        "Range"       : (1, 127),
        "GetDisplay"  : lambda prof, v: v / 1.28,
        "SetDisplay"  : lambda prof, v: round (v * 1.28),
    },

    "ReverseSpeed" :
    {
        "Type"        : "i",
        "Name"        : _("Reverse speed"),
        "Description" : _("""\
The speed at which motor runs in reverse direction when the DX3 \
board contact is connected to ground.\
"""),
        "Default"     : 35,
        "Units"       : "%",
        "Widget"      : infineon.PWT_SPINBUTTON,
        "Precision"   : 1,
        "Range"       : (1, 191),
        "GetDisplay"  : lambda prof, v: v / 1.91,
        "SetDisplay"  : lambda prof, v: round (v * 1.91),
    },

    "BlockTime" :
    {
        "Type"        : "f",
        "Name"        : _("Overcurrent detection delay"),
        "Description" : _("""\
The amount of time before the phase current limit takes effect  \
Rising this parameter will help you start quicker from a dead stop, \
but don't set this too high as you risk blowing out your motor - \
at high currents it will quickly heat up. Set it to 0 to disable overcurrent. \
"""),
        "Default"     : 1.0,
        "Units"       : _("s"),
        "Widget"      : infineon.PWT_SPINBUTTON,
        "Range"       : (0, 100),
        "GetDisplay"  : lambda prof, v: v / 10,
        "SetDisplay"  : lambda prof, v: round (v * 10),
    },

    "AutoCruisingTime" :
    {
        "Type"        : "f",
        "Name"        : _("Auto cruising time"),
        "Description" : _("""\
The amount of seconds to hold the throttle position unchanged \
before the 'cruising' mode will be enabled. For this to work \
you need to connect the CR contact on the board to ground.\
"""),
        "Default"     : 15.0,
        "Units"       : _("s"),
        "Widget"      : infineon.PWT_SPINBUTTON,
        "Range"       : (10, 150),
        "GetDisplay"  : lambda prof, v: v / 10,
        "SetDisplay"  : lambda prof, v: round (v * 10),
    },

    "SlipChargeMode" :
    {
        "Type"        : "i",
        "Name"        : _("Slip charge mode"),
        "Description" : _("""\
This parameter controls regen from the throttle. If you enable it, \
throttling back will enable regen (and thus will brake) until the \
electronic braking becomes ineffective (at about 15% of full speed).\
"""),
        "Default"     : SCM_DISABLE,
        "Widget"      : infineon.PWT_COMBOBOX,
        "Range"       : (0, 1),
        "GetDisplay"  : lambda prof, v: SlipChargeModeDesc [v],
    },

    "LimitCruise" :
    {
        "Type"        : "i",
        "Name"        : _("Limit cruise"),
        "Description" : _("""\
So far it is unknown how this parameter affects controller function.\
"""),
        "Default"     : 0,
        "Widget"      : infineon.PWT_COMBOBOX,
        "Range"       : (0, 1),
        "GetDisplay"  : lambda prof, v: CruiseLimitDesc [v],
    },

    "IndicatorMode" :
    {
        "Type"        : "i",
        "Name"        : _("LED indicator mode"),
        "Description" : _("""\
This sets the mode of the P1, P2 and P3 contacts on the board. \
The connected LEDs may use either a common GND or common VCC.\
"""),
        "Default"     : IM_COMM_GND,
        "Widget"      : infineon.PWT_COMBOBOX,
        "Range"       : (0, 1),
        "GetDisplay"  : lambda prof, v: IndicatorModeDesc [v],
    },

    "EBSLevel" :
    {
        "Type"        : "i",
        "Name"        : _("EBS level"),
        "Description" : _("""\
Electronic braking level. Choose 'Moderate' for smaller wheel diameters, \
and 'Strong' for 26" and up. In 'Unlimited' mode controller does not impose \
any limits on braking strength; this is a undocumented feature and is \
not guaranteed to work with your controller. The larger is the level, \
the more effective is braking.\
"""),
        "Default"     : EBS_DISABLED,
        "Widget"      : infineon.PWT_COMBOBOX,
        "Range"       : (0, 3),
        "GetDisplay"  : lambda prof, v: EBSLevelDesc [v],
        # This member, if defined, tells how to translate setting to raw value
        "ToRaw"       : lambda prof, v: EBSLevel2Raw [v],
    },

    "EBSLimVoltage" :
    {
        "Type"        : "f",
        "Name"        : _("EBS limit voltage"),
        "Description" : _("""\
When regen is enabled (also known as electronic braking system) \
the controller effectively acts as a step-up DC-DC converter, \
transferring energy from the motor into the battery. This sets \
the upper voltage limit for this DC-DC converter, which is needed \
to prevent blowing out the controller MOSFETs.\
"""),
        "Default"     : 75,
        "Depends"     : [ "ControllerType" ],
        "Units"       : _("V"),
        "Widget"      : infineon.PWT_SPINBUTTON,
        "Range"       : (1, 255),
        "GetDisplay"  : lambda prof, v: prof.GetController () ["Raw2Voltage"] (v),
        "SetDisplay"  : lambda prof, v: round (prof.GetController () ["Voltage2Raw"] (v)),
    },

    "GuardLevel" :
    {
        "Type"        : "i",
        "Name"        : _("Guard signal polarity"),
        "Description" : _("""\
The polarity of the Guard signal, which should be connected to the \
TB pin on the board  When Guard is active, controller will prevent \
rotating the wheel in any direction. This is useful if used together \
with a motorcycle alarm or something like that.\
"""),
        "Default"     : GP_LOW,
        "Widget"      : infineon.PWT_COMBOBOX,
        "Range"       : (0, 1),
        "GetDisplay"  : lambda prof, v: GuardLevelDesc [v],
    },

    "ThrottleProtect" :
    {
        "Type"        : "i",
        "Name"        : _("Throttle blowout protect"),
        "Description" : _("""\
Enable this parameter to let the controller check if your \
throttle output is sane (e.g. if the Hall sensor in the throttle \
is not blown out). If it is broken, you might get a constant \
full-throttle condition, which might be not very pleasant.\
"""),
        "Default"     : TBP_ENABLE,
        "Widget"      : infineon.PWT_COMBOBOX,
        "Range"       : (0, 1),
        "GetDisplay"  : lambda prof, v: ThrottleProtectDesc [v],
    },

    "PASMode" :
    {
        "Type"        : "i",
        "Name"        : _("PAS mode"),
        "Description" : _("""\
Pedal Assisted Sensor mode.\
"""),
        "Default"     : PAS_FAST,
        "Widget"      : infineon.PWT_COMBOBOX,
        "Range"       : (0, 1),
        "GetDisplay"  : lambda prof, v: PASModeDesc [v],
    },

    "PASStartPulse" :
    {
        "Type"        : "i",
        "Name"        : _("PAS start pulse"),
        "Description" : _("""\
The amount of pulses from the PAS sensor to skip before starting assisting \
to pedalling.\
"""),
        "Default"     : 3,
        "Widget"      : infineon.PWT_SPINBUTTON,
        "Range"       : (2, 255),
        "Precision"   : 0,
        "ToRaw"       : lambda prof, v: v - 2,
        "SetDisplay"  : lambda prof, v: v,
        "GetDisplay"  : lambda prof, v: v,
    },

    "PASMaxSpeed" :
    {
        "Type"        : "i",
        "Name"        : _("PAS max speed"),
        "Description" : _("""\
This sets the speed limit when using the pedal assistant.\
"""),
        "Default"     : 100,
        "Units"       : "%",
        "Widget"      : infineon.PWT_SPINBUTTON,
        "Precision"   : 1,
        "Range"       : (1, 191),
        "GetDisplay"  : lambda prof, v: v / 1.91,
        "SetDisplay"  : lambda prof, v: round (v * 1.91),
    },

    "DefaultSpeed" :
    {
        "Type"        : "i",
        "Name"        : _("Default speed"),
        "Description" : _("""\
This determines which of the four programmed speed limits will be default \
after power on.\
"""),
        "Default"     : 1,
        "Widget"      : infineon.PWT_COMBOBOX,
        "Range"       : (0, 3),
        "GetDisplay"  : lambda prof, v: DefaultSpeedDesc [v],
    },

    "SensorAngle" :
    {
        "Type"        : "i",
        "Name"        : _("Hall sensors angle"),
        "Description" : _("""\
The (electric) angle between Hall sensors in your motor. Most \
motors use sensors at 120 degrees, but sometimes this may differ. \
Choose "Auto" if you want the controller to detect this \
automatically.\
"""),
        "Default"     : SA_COMPAT,
        "Widget"      : infineon.PWT_COMBOBOX,
        "Range"       : (0, 2),
        "GetDisplay"  : lambda prof, v: SensorAngleDesc [v],
    },
}

# -- # -- # -- # -- # -- # -- # -- # -- # -- # -- # -- # -- #

class Profile (infineon.Profile):

    # Parameter order when loading from .asv files
    ParamLoadOrder = [
        "ControllerType", "PhaseCurrent", "BatteryCurrent", "HaltVoltage", \
        "VoltageTolerance", "LimitedSpeed", "SpeedSwitchMode", "Speed1", "Speed2", \
        "Speed3", "BlockTime", "AutoCruisingTime", "SlipChargeMode", \
        "IndicatorMode", "EBSLevel", "ReverseSpeed", "EBSLimVoltage", \
        "GuardLevel", "ThrottleProtect", "PASMode", "PASStartPulse", \
        "DefaultSpeed", "Speed4", "SensorAngle", "PASMaxSpeed", "LimitCruise"
    ]

    # The order of parameters in the profile edit dialog
    ParamEditOrder = [
        [ _("Hardware type") ],
        "ControllerType",

        [ _("Current/Voltage design") ],
        "BatteryCurrent",
        "PhaseCurrent",
        "BlockTime",
        "HaltVoltage",
        "VoltageTolerance",

        [ _("Speed modes") ],
        "SpeedSwitchMode",
        "Speed1",
        "Speed2",
        "Speed3",
        "Speed4",
        "DefaultSpeed",
        "LimitedSpeed",
        "ReverseSpeed",

        [ _("Regeneration") ],
        "EBSLevel",
        "EBSLimVoltage",
        "SlipChargeMode",

        [ _("Pedal Assist Sensor") ],
        "PASMode",
        "PASStartPulse",
        "PASMaxSpeed",

        [ _("External devices") ],
        "SensorAngle",
        "AutoCruisingTime",
        "GuardLevel",
        "ThrottleProtect",
        "IndicatorMode",
    ]

    # The order of parameters in raw binary data sent to controller
    ParamRawOrder = [
        2,
        15,
        "PhaseCurrent",
        "BatteryCurrent",
        "HaltVoltage",
        "VoltageTolerance",
        "LimitedSpeed",
        "SpeedSwitchMode",
        "Speed1",
        "Speed2",
        "Speed3",
        "BlockTime",
        "AutoCruisingTime",
        "SlipChargeMode",
        "IndicatorMode",
        "EBSLevel",
        "ReverseSpeed",
        "EBSLimVoltage",
        "GuardLevel",
        "ThrottleProtect",
        "PASMode",
        "PASStartPulse",
        "DefaultSpeed",
        "Speed4",
        "SensorAngle",
        "PASMaxSpeed",
        "LimitCruise",
        3,
        0,
        0,
        0,
    ]


    def __init__ (self, Family, FileName):
        infineon.Profile.__init__ (self, Family, FileName, \
            ControllerTypeDesc, ControllerParameters)


    def Upload (self, com_port, progress_func):
        data = self.BuildRaw ()

        try:
            ser = serial.Serial (com_port, 38400, serial.EIGHTBITS, serial.PARITY_NONE,
                serial.STOPBITS_TWO, timeout=0.2)
        except serial.SerialException, e:
            raise serial.SerialException (str (e).decode (locale.getpreferredencoding ()))

        progress_func (msg = _("Waiting for controller ready"))
        # Send '8's and wait for the 'U' response
        skip_write = False
        while True:
            if not skip_write:
                # Garbage often comes from the controller upon bootup, just ignore it
                ser.flushInput ()
                ser.write ('8')
            skip_write = False

            c = ser.read ()
            if c == 'U':
                break

            if len (c) > 0:
                skip_write = True

            if not progress_func ():
                return False

        progress_func (msg = _("Waiting acknowledgement"))

        ser.flushInput ()
        ser.write (str (data))
        ack = "QR"
        while True:
            c = ser.read ()
            while len (c) and (c [0] == ack [0]):
                c = c [1:]
                ack = ack [1:]
                if len (ack) == 0:
                    return True

            if len (c) > 0:
                if c [0] == chr (0xa2):
                    raise Exception (_("Controller says received data is broken"))
                raise Exception (_("Invalid reply byte '%(chr)02x'") % { "chr" : ord (c [0]) })

            if not progress_func ():
                break

        return False


def DetectFormat3 (l):
    if len (l) < 26:
        return False

    i = l [0].find (':')
    if i >= 0:
        ct = l [0][i + 1:]
        if (ct != "") and (ct [:3] != "EB3"):
            return False

    return True


infineon.RegisterFamily (_("Infineon 3"), Profile, DetectFormat3, \
    (x ["Name"] for x in ControllerTypeDesc))
