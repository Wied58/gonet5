
import time
from picamera2 import Picamera2, Preview
from libcamera import controls
from pprintpp import pprint as pp

#import picamera2

#from PIL import Image
from PIL import Image, ExifTags
import numpy as np


#**************************************


import piexif

def add_geolocation(image_path, latitude, longitude):
    exif_dict = piexif.load(image_path)

    # Convert latitude and longitude to degrees, minutes, seconds format
    def deg_to_dms(deg):
        d = int(deg)
        m = int((deg - d) * 60)
        s = int(((deg - d) * 60 - m) * 60)
        return ((d, 1), (m, 1), (s, 1))

    lat_dms = deg_to_dms(latitude)
    lon_dms = deg_to_dms(longitude)

    exif_dict["GPS"][piexif.GPSIFD.GPSLatitude] = lat_dms
    exif_dict["GPS"][piexif.GPSIFD.GPSLongitude] = lon_dms
    exif_dict["GPS"][piexif.GPSIFD.GPSLatitudeRef] = 'N' if latitude >= 0 else 'S'
    exif_dict["GPS"][piexif.GPSIFD.GPSLongitudeRef] = 'E' if longitude >= 0 else 'W'

    exif_bytes = piexif.dump(exif_dict)
    piexif.insert(exif_bytes, image_path)

    print("Geolocation data added to", image_path)


#*************************************


picam2 = Picamera2()


#picam2.controls.FrameDurationLimits = (100, 1000000)
picam2.controls.FrameDurationLimits = (100, 240000000)

#picam2.controls.ExposureTime = 239542228
picam2.controls.ExposureTime = 1000000

config = picam2.create_still_configuration(raw={"size": (4032, 3024)})
picam2.configure(config)

picam2.iso = 800 


time.sleep(2)
picam2.start()


metadata = picam2.capture_metadata()
pp(metadata)


# Capture an image as a NumPy array
array = picam2.capture_array()

print(f"the array shape is : {array.shape}")

# Convert the array to a PIL Image object
img = Image.fromarray(array)

# Save the image as a TIFF file

img.save("image.tiff")

img.save("image.jpg")

SensTemp = metadata["SensorTemperature"]
print(f"SensorTemperature = {SensTemp}")

picam2.close()



latitude = 34.0522  # Example latitude coordinates
longitude = -118.2437  # Example longitude coordinates
image_path = 'image.jpg'  # Path to your image

add_geolocation(image_path, latitude, longitude)

image_path = 'image.tiff'  # Path to your image

add_geolocation(image_path, latitude, longitude)




