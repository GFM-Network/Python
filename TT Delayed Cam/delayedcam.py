import cv2
from collections import deque

# Function to update the buffer with new frame
def update_buffer(frame):
    if len(buffer) == buffer_size:
        buffer.popleft()  # Remove the oldest frame if buffer is full
    buffer.append(frame)

# Function to get the frame from 6 seconds ago
def get_past_frame():
    if len(buffer) >= fps * 6:  # Check if there are enough frames in the buffer
        return buffer[-(fps * 6)]
    else:
        return None

# Constants
buffer_size = 180  # 6 seconds buffer at 30 fps
fps = 30

# Initialize video capture
cap = cv2.VideoCapture(0)

# Get the default screen resolution
screen_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
screen_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Create buffer to store frames
buffer = deque(maxlen=buffer_size)

while True:
    ret, frame = cap.read()

    if ret:
        update_buffer(frame)

        past_frame = get_past_frame()

        if past_frame is not None:
            # Resize the frame to match screen resolution
            resized_frame = cv2.resize(past_frame, (screen_width, screen_height))

            # Show the frame from 6 seconds ago in fullscreen mode
            cv2.namedWindow('Past Frame', cv2.WINDOW_NORMAL)
            cv2.setWindowProperty('Past Frame', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            cv2.imshow('Past Frame', resized_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release video capture and close windows
cap.release()
cv2.destroyAllWindows()
