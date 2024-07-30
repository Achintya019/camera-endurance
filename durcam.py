import cv2
import time
from datetime import datetime
import os

cam_index = 0
cap = cv2.VideoCapture(cam_index)  
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

csv_path = 'log_camera.csv'
update_interval = 5  # Update CSV every 'x' seconds

# Start time to calculate the duration
start_time = time.time()
latest_frame = None
last_update_time = start_time

# Track the filename of the last saved image
last_image_filename = None

# Create or open the CSV file and write the headers if it doesn't exist
if not os.path.isfile(csv_path):
    with open(csv_path, 'w') as f:
        f.write('date,duration,image_path\n')

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Can't receive frame. Exiting ...")
            break

        # Store the latest frame
        latest_frame = frame

        cv2.imshow('frame', frame)

        # Update the CSV file periodically
        current_time = time.time()
        if current_time - last_update_time >= update_interval:
            duration_seconds = current_time - start_time
            duration_hours = duration_seconds / 3600

            # Generate timestamp for image filename
            timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            image_filename = f'{timestamp}.jpg'

            # Delete the previous image file if it exists
            if last_image_filename and os.path.isfile(last_image_filename):
                os.remove(last_image_filename)

            # Save the latest frame with the timestamped filename
            if latest_frame is not None:
                cv2.imwrite(image_filename, latest_frame)
                last_image_filename = image_filename  # Update the last image filename

            # Write the latest duration and image path to the CSV file
            with open(csv_path, 'w') as f:
                f.write('date,duration,image_path\n')  # Write headers
                f.write(f'{datetime.now().strftime("%Y-%m-%d")},{duration_hours:.2f} hours,{image_filename}\n')

            last_update_time = current_time  # Update the last update time

        # Press 'q' to exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    pass

# Calculate the final duration for which the camera was running
end_time = time.time()
duration_seconds = end_time - start_time
duration_hours = duration_seconds / 3600
print(f"Camera was running for {duration_hours:.2f} hours.")

# Save the last image with a timestamp
final_image_filename = datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.jpg'
if latest_frame is not None:
    cv2.imwrite(final_image_filename, latest_frame)

# Write the final date, duration, and image path to the CSV file
with open(csv_path, 'w') as f:
    f.write('date,duration,image_path\n')  # Write headers
    f.write(f'{datetime.now().strftime("%Y-%m-%d")},{duration_hours:.2f} hours,{final_image_filename}\n')

# Release the camera and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
