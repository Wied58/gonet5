
import time
from datetime import datetime

from picamera2 import Picamera2, Preview
from libcamera import controls
from pprintpp import pprint as pp

import picamera2

from PIL import Image
from PIL import Image, ExifTags
import numpy as np
import piexif

# exposure time in micro seconds
exposure = 1000000



picam2 = Picamera2()


config = picam2.create_still_configuration(raw={"size": (4032, 3024)})
picam2.configure(config)

picam2.set_controls({ 
                     "ExposureTime": exposure,  
                     "AnalogueGain": 8.0, 
                     "AeEnable": False, 
                     "AwbEnable": False
                     })


time.sleep(2)
picam2.start()

picam2.controls.FrameDurationLimits = (100, 240000000)


metadata = picam2.capture_metadata()
pp(metadata)
print()
pp(picam2.camera_controls)

# Capture an image as a NumPy array
array = picam2.capture_array()

print(f"the array shape is : {array.shape}")

#  Convert the array to a PIL Image object
img = Image.fromarray(array)

# Save the image as a TIFF file

img.save("image.tiff")

img.save("image.jpg")

SensTemp = metadata["SensorTemperature"]
print(f"SensorTemperature = {SensTemp}")

picam2.close()

#*******************
# EXIF
# from: https://stackoverflow.com/questions/52729428/how-to-write-custom-metadata-into-jpeg-with-python
# Tag references:
# https://exiftool.org/TagNames/EXIF.html
# https://www.media.mit.edu/pia/Research/deepview/exif.html

import piexif

total_gain = metadata["AnalogueGain"] * metadata["DigitalGain"]
datetime_now = datetime.now().strftime("%Y:%m:%d %H:%M:%S")

# set up exif_dictionary

zeroth_ifd = {
              piexif.ImageIFD.Make: u"Canon",
              piexif.ImageIFD.XResolution: (96, 1),
              piexif.ImageIFD.YResolution: (96, 1),
              piexif.ImageIFD.Software: u"piexif"
              }
exif_ifd = {
            piexif.ExifIFD.DateTimeOriginal: datetime_now,
            piexif.ExifIFD.ExposureTime: (metadata["ExposureTime"], 1000000),
            piexif.ExifIFD.ISOSpeedRatings: int(total_gain * 100),
            }
gps_ifd = {
           piexif.GPSIFD.GPSVersionID: (2, 0, 0, 0),
           piexif.GPSIFD.GPSAltitudeRef: 1,
           piexif.GPSIFD.GPSDateStamp: u"1999:99:99 99:99:99",
           }
first_ifd = {
             piexif.ImageIFD.Make: u"Canon",
             piexif.ImageIFD.XResolution: (40, 1),
             piexif.ImageIFD.YResolution: (40, 1),
             piexif.ImageIFD.Software: u"piexif"
             }

#exif_dict = {"0th":zeroth_ifd, "Exif":exif_ifd, "GPS":gps_ifd, "1st":first_ifd, "thumbnail":thumbnail}
exif_dict = {"0th":zeroth_ifd, "GPS":gps_ifd, "Exif":exif_ifd, "1st":first_ifd}

pp(exif_dict)

exif_bytes = piexif.dump(exif_dict)

print()
print(exif_bytes)

#
im = Image.open("image.jpg")
im.save("out.jpg", exif=exif_bytes)
#
im = Image.open("image.tiff")
im.save("out.tiff", exif=exif_bytes)


