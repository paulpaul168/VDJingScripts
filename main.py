import cv2
import numpy as np
import NDIlib as ndi
import serial

lower_bound = np.array([0, 100, 100])
upper_bound = np.array([10, 255, 255])

if not ndi.initialize():
    exit()

ndi_find = ndi.find_create_v2()

if ndi_find is None:
    exit()

sources = []
while not len(sources) > 0:
    print('Looking for sources ...')
    ndi.find_wait_for_sources(ndi_find, 3000)
    sources = ndi.find_get_current_sources(ndi_find)

ndi_recv_create = ndi.RecvCreateV3()
ndi_recv_create.color_format = ndi.RECV_COLOR_FORMAT_BGRX_BGRA

ndi_recv = ndi.recv_create_v3(ndi_recv_create)

if ndi_recv is None:
    exit()

for i, s in enumerate(sources):
    print('%s. %s' % (i + 1, s.ndi_name))
ndi.recv_connect(ndi_recv, sources[0])

ndi.find_destroy(ndi_find)

ndi_send = ndi.send_create()

if ndi_send is None:
    exit()

video_frame = ndi.VideoFrameV2()
img = np.zeros((1080, 1920, 4), dtype=np.uint8)
video_frame.data = img
video_frame.FourCC = ndi.FOURCC_VIDEO_TYPE_BGRX

# Initialize serial communication
ser = serial.Serial('COM7', 9600)

while True:
    # Read serial data
    line = ser.readline().decode().strip()
    try:
        # Parse RGB values from the line
        r, g, b = map(int, line.split(':')[1].strip().split(','))
        print(f"Received RGB values: {r}, {g}, {b}")
        # Update lower and upper bounds based on the received RGB values
        lower_bound = np.array([r, g, b])
        upper_bound = np.array([r+10, 255, 255])
    except:
        # Ignore badly formatted lines
        continue

    # Receive the next frame from the NDI source
    t, v, _, _ = ndi.recv_capture_v2(ndi_recv, 5000)
    if t == ndi.FRAME_TYPE_VIDEO:
        print('Video data received (%dx%d).' % (v.xres, v.yres))
        frame = np.copy(v.data)
        # Convert the frame to the HSV color space
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Create a mask that filters out colors that are outside the defined bounds
        mask = cv2.inRange(hsv, lower_bound, upper_bound)

        # Use the mask to extract only the filtered colors from the frame
        filtered_frame = cv2.bitwise_and(frame, frame, mask=mask)

        video_frame.data = filtered_frame
        # Send the filtered frame to the NDI destination
        ndi.send_send_video_v2(ndi_send, video_frame)
        ndi.recv_free_video_v2(ndi_recv, v)

ndi.recv_destroy(ndi_recv)
ndi.send_destroy(ndi_send)
ndi.destroy()
