# Infineon 2 parameters #

|Controller type|The type of your controller. This influences the coefficients assumed for various parts of the controller, e.g. shunts, resistive dividers. If you have a non-standard controller, you may create your own type in infineon.py|
|:--------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|Phase current limit|The current limit in motor phase wires. Since the e-bike controller is, in a sense, a step-down DC-DC converter, the motor current can actually be much higher than the battery current. When setting this parameter, make sure you don't exceed the capabilities of the MOSFETs in your controller. This parameter mostly affects the acceleration on low speeds.|
|Battery current limit|The limit for the current drawn out of the battery. Make sure this does not exceed the specs for your battery, otherwise you will lose a lot of energy heating up the battery (and may blow it, too).|
|Battery low voltage|The voltage at which controller cuts of the power. Make sure this is at least equal to lowest\_cell\_voltage x cell\_count (e.g. for a 12S LiFePO4 battery this would be `2.6 * 12 = 31.2V`). This does not matter much if you use a BMS, since it will cut the power as soon as **any** cell reaches the lowest voltage, which is much better for the health of your battery.|
|Battery low voltage threshold|The amount of volts for the battery voltage to rise after a cutoff due to low voltage for the controller to restore power back. This is most useful for plumbum batteries, as they tend to restore voltage after a bit of rest.|
|Limited speed|The speed corresponding to 100% throttle when the 'speed limit' switch/wires are enabled (when the 'SL' board contact is connected to ground).|
|Speed switch mode|The way how the speed switch functions. When in 'Switch' mode you may use a three-position switch which connects X1 (speed 1) or X2 (speed 3) to GND, or leaves both unconnected (speed 2). In 'Cycle' mode connecting X1 to ground with a momentary switch will toggle between speeds 1, 2 and 3 (speed 1 is default after power-on).|
|Speed 1|The first speed limit.(see comment to 'speed switch mode').|
|Speed 2|The second speed limit.(see comment to 'speed switch mode').|
|Speed 3|The third speed limit.(see comment to 'speed switch mode').|
|Overcurrent detection delay|The amount of time before the phase current limit takes effect  Rising this parameter will help you start quicker from a dead stop, but don't set this too high as you risk blowing out your motor - at high currents it will quickly heat up. Set it to 0 to disable overcurrent. |
|Auto cruising time|The amount of seconds to hold the throttle position unchanged before the 'cruising' mode will be enabled. For this to work you need to connect the CR contact on the board to ground.|
|Slip charge mode|This parameter controls regen from the throttle. If you enable it, throttling back will enable regen (and thus will brake) until the electronic braking becomes ineffective (at about 15% of full speed).|
|LED indicator mode|This sets the mode of the P1, P2 and P3 contacts on the board. The connected LEDs may use either a common GND or common VCC.|
|EBS level|Electronic braking level. Choose 'Moderate' for smaller wheel diameters, and 'Strong' for 26" and up. In 'Unlimited' mode controller does not impose any limits on braking strength; this is a undocumented feature and is not guaranteed to work with your controller. The larger is the level, the more effective is braking.|
|Reverse speed|The speed at which motor runs in reverse direction when the DX3 board contact is connected to ground.|
|EBS limit voltage|When regen is enabled (also known as electronic braking system) the controller effectively acts as a step-up DC-DC converter, transferring energy from the motor into the battery. This sets the upper voltage limit for this DC-DC converter, which is needed to prevent blowing out the controller MOSFETs.|
|Guard signal polarity|The polarity of the Guard signal, which should be connected to the TB pin on the board  When Guard is active, controller will prevent rotating the wheel in any direction. This is useful if used together with a motorcycle alarm or something like that.|
|Throttle blowout protect|Enable this parameter to let the controller check if your throttle output is sane (e.g. if the Hall sensor in the throttle is not blown out). If it is broken, you might get a constant full-throttle condition, which might be not very pleasant.|
|PAS mode|The time motor is running after last PAS impulse.|
|P3 mode|An additional setting for the P3 LED output. You may select between displaying only the "Cruise" mode on this LED, or both "Cruise" and fault conditions.|
|Hall sensors angle|The (electric) angle between Hall sensors in your motor. Most motors use sensors at 120 degrees, but sometimes this may differ. Choose "Auto" if you want the controller to detect this automatically.|

# Infineon 3 parameters #

|Controller type|The type of your controller. This influences the coefficients assumed for various parts of the controller, e.g. shunts, resistive dividers. If you have a non-standard controller, you may create your own type in infineon.py|
|:--------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|Phase current limit|The current limit in motor phase wires. Since the e-bike controller is, in a sense, a step-down DC-DC converter, the motor current can actually be much higher than the battery current. When setting this parameter, make sure you don't exceed the capabilities of the MOSFETs in your controller. This parameter mostly affects the acceleration on low speeds.|
|Battery current limit|The limit for the current drawn out of the battery. Make sure this does not exceed the specs for your battery, otherwise you will lose a lot of energy heating up the battery (and may blow it, too).|
|Battery low voltage|The voltage at which controller cuts of the power. Make sure this is at least equal to lowest\_cell\_voltage x cell\_count (e.g. for a 12S LiFePO4 battery this would be `2.6 * 12 = 31.2V`). This does not matter much if you use a BMS, since it will cut the power as soon as **any** cell reaches the lowest voltage, which is much better for the health of your battery.|
|Battery low voltage threshold|The amount of volts for the battery voltage to rise after a cutoff due to low voltage for the controller to restore power back. This is most useful for plumbum batteries, as they tend to restore voltage after a bit of rest.|
|Limited speed|The speed corresponding to 100% throttle when the 'speed limit' switch/wires are enabled (when the 'SL' board contact is connected to ground).|
|Speed switch mode|The way how the speed switch functions. When in 'Switch' mode you may use a three-position switch which connects X1 (speed 1) or X2 (speed 3) to GND, or leaves both unconnected (speed 2). In 'Cycle 3' mode connecting X1 to ground with a momentary switch will cycle speeds 1-2-3. The 'High Switch' mode is similar to 'Switch', but X1/X2 should connect to high voltage (+5V or +BAT). The 'Cycle 4' mode is like 'Cycle 3', but cycles between speeds 1-2-3-4.|
|Speed 1|The first speed limit (see comment to 'speed switch mode').|
|Speed 2|The second speed limit (see comment to 'speed switch mode').|
|Speed 3|The third speed limit (see comment to 'speed switch mode').|
|Overcurrent detection delay|The amount of time before the phase current limit takes effect  Rising this parameter will help you start quicker from a dead stop, but don't set this too high as you risk blowing out your motor - at high currents it will quickly heat up. Set it to 0 to disable overcurrent. |
|Auto cruising time|The amount of seconds to hold the throttle position unchanged before the 'cruising' mode will be enabled. For this to work you need to connect the CR contact on the board to ground.|
|Slip charge mode|This parameter controls regen from the throttle. If you enable it, throttling back will enable regen (and thus will brake) until the electronic braking becomes ineffective (at about 15% of full speed).|
|LED indicator mode|This sets the mode of the P1, P2 and P3 contacts on the board. The connected LEDs may use either a common GND or common VCC.|
|EBS level|Electronic braking level. Choose 'Moderate' for smaller wheel diameters, and 'Strong' for 26" and up. In 'Unlimited' mode controller does not impose any limits on braking strength; this is a undocumented feature and is not guaranteed to work with your controller. The larger is the level, the more effective is braking.|
|Reverse speed|The speed at which motor runs in reverse direction when the DX3 board contact is connected to ground.|
|EBS limit voltage|When regen is enabled (also known as electronic braking system) the controller effectively acts as a step-up DC-DC converter, transferring energy from the motor into the battery. This sets the upper voltage limit for this DC-DC converter, which is needed to prevent blowing out the controller MOSFETs.|
|Guard signal polarity|The polarity of the Guard signal, which should be connected to the TB pin on the board  When Guard is active, controller will prevent rotating the wheel in any direction. This is useful if used together with a motorcycle alarm or something like that.|
|Throttle blowout protect|Enable this parameter to let the controller check if your throttle output is sane (e.g. if the Hall sensor in the throttle is not blown out). If it is broken, you might get a constant full-throttle condition, which might be not very pleasant.|
|PAS mode|Pedal Assisted Sensor mode.|
|PAS start pulse|The amount of pulses from the PAS sensor to skip before starting assisting to pedalling.|
|Default speed|This determines which of the four programmed speed limits will be default after power on.|
|Speed 4|The fourth speed limit (see comment to 'speed switch mode').|
|Hall sensors angle|The (electric) angle between Hall sensors in your motor. Most motors use sensors at 120 degrees, but sometimes this may differ. Choose "Auto" if you want the controller to detect this automatically.|
|PAS max speed|This sets the speed limit when using the pedal assistant.|
|Limit cruise|So far it is unknown how this parameter affects controller function.|