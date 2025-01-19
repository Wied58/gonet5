This repo represent the intial experiments for rewriting GONet4 with the Picamera2 module. It is olny inteneted to share my finds with the rest of the group. 

Calling the repo and the main script "GONet5.py" may be a bit premature, however, I'm placing my creativity elsewhere at the monent.




Picamera2 is not a compatible port of Picamera. The operation and parameters are completely different. 

The main difference is that as opposed to taking a jpeg with an option to include the raw sensor data in one file from the same data, I'm collecting to image data to a numpy array and using PIL to create separate image file for jpeg and TIFF. EXIF meta data is added to the image files via the piexif module. Having the data in the numpy array also allows us to use astropy to create FITS images. (At this time, I don't belive piexif can save meta to FITS, and I don't know much about astropy. However, if FITS images are desired, I'll learn.)

I have been reviewing the parameters used in Picamera and looking for the Picamera 2 counter parts. 


gonet4 picamera settings used in gonet4:

* DRC: off
In image processing, "dynamic range compression" refers to a technique that reduces the difference between the brightest and darkest areas of an image.

https://forums.raspberrypi.com/viewtopic.php?t=140917 "Problem is that when I set drc_strength to anything other than 'off', the manual white balance settings seem to have no effect."

I do not believe there is a Picamera equivalent at this time. 

* ISO: usually set to 800 in gonet4
The picamera2 GitHub examples defines ISO as:

AnalogueGain*DigitalGain*100

total_gain = metadata["AnalogueGain"] * metadata["DigitalGain"]
piexif.ExifIFD.ISOSpeedRatings: int(total_gain * 100)

Per the Picamera Docs, DigitalGain is defined as "Digital gain is used automatically when the sensor’s analogue gain control cannot go high enough, and so this value is only reported in captured image metadata. It cannot be set directly - users should set the AnalogueGain instead and digital gain will be used when needed."

I'm not sure what would change the value of DigitalGain.

From the test runs, DigitalGain is set at 1.0, therefore setting AnalogueGain to 8.0 will yield an ISO of 800. 

There are references from a google search that explain the differences between gain and ISO.

* White Balance. 

White balance is a form of color correction. They way I think it works is that the the lightest pixel in the array is discovered and by what ever red and blue values are contained within that lightest pixel are subtracted are subtracted from every pixel in the array. 

In gonet4 awb (auto white balance) is set to off and we manually set the white_balance_gains = (3.35, 1.59). 

These numbers were set to ensure the camera had something consistent to work with. The values were determined by simulating darkness in the machine room in the Adler lab. 

In Picamera2 there is a parameter AwbEnable to disable awb. The documentation also has a parameter, ColourGains. However it a range of 0 to 32 as opposed to 0.0 and 8.0 in the old Picamera.

I set the test script to the old values, just to test the syntax, however, I propose we discuss setting the values to zero or rerun the machine room experiment. 

* Brightness

in gonet4 brightness was set to 50. In Picamera2 the allowable values are -1.0 to 1.0. I'm not sure how this translates at this time.

* exposure_mode
We set exposure mode to off in gonet4. I think we were experimenting with trying to get the camera to quit wasting time metering when we set values manually. 

* still_stats = True

From: https://picamera.readthedocs.io/

When this property is False (the default), statistics will be calculated from the preceding preview frame (this also applies when the preview is not visible). When True, statistics will be calculated from the captured image itself




Other random notes:

GIacomo's wish list:
https://docs.google.com/document/d/1xOE8KZca4Cpi7TNhzkWXP5ZyzEa4UlTLSsKll-m6elE/edit?tab=t.0




The SensorTemperature control will only be returned in metadata if a themal sensor is present.


needed for picamera installtion: sudo chmod og+rx /home/*



Move unprocessed to beginning of script
Unprocessed images should be labeled in filename, exif or both. 


