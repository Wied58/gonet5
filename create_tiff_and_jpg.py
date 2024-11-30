
import time
from picamera2 import Picamera2, Preview
from libcamera import controls
from pprintpp import pprint as pp

#import picamera2
from PIL import Image
import numpy as np



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


picam2.close()




