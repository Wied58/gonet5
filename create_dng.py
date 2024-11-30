#!/usr/bin/python3
# Capture a JPEG while still running in the preview mode. When you
# capture to a file, the return value is the metadata for that image.
import time
from picamera2 import Picamera2, Preview
from libcamera import controls

picam2 = Picamera2()

picam2.configure("preview")

#picam2.set_controls({"FrameDurationLimits": (100, 50000000), 'ExposureTime': 1000000})

picam2.controls.FrameDurationLimits = (100, 1000000)

picam2.controls.ExposureTime = 239542228

picam2.iso = 800 


time.sleep(2)


#preview_config = picam2.create_preview_configuration(main={"size": (800, 600)})
#picam2.configure(preview_config)
#picam2.start_preview(Preview.QTGL)

#picam2.start(show_preview=False)

picam2.start()
time.sleep(2)

#picam2.capture_file("test.jpg")
metadata = picam2.capture_file("test.jpg", 'raw')

print(metadata)
picam2.close()
