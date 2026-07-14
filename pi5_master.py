import cv2
import numpy as np
import subprocess
import os
import serial
import time
from ultralytics import YOLO

# Force X11 for RealVNC compatibility
os.environ["QT_QPA_PLATFORM"] = "xcb"

# --- 1. INITIALIZATION ---
print("--- [1/3] Loading AI Core ---")
# Ensure 'yolov8n_ncnn_model' is in the same folder
model = YOLO('yolov8n_ncnn_model', task='detect')

print("--- [2/3] Connecting to Pico W ---")
try:
    pico = serial.Serial('/dev/ttyACM0', 115200, timeout=0.01)
    print("[SUCCESS] Pico W Connected.")
except Exception as e:
    pico = None
    print(f"[WARNING] Pico W not found: {e}")

# --- 2. THE RPICAM PIPE (FIXED CMD) ---
print("--- [3/3] Starting rpicam-vid ---")

rpicam_cmd = [
    'rpicam-vid',
    '-t', '0',                # This is the timeout (0 = forever)
    '--width', '640',
    '--height', '480',
    '--framerate', '15',
    '--codec', 'mjpeg',
    '--inline',
    '--nopreview',
    '--flush',
    '--bitrate', '1000000',   # Keep network traffic low for VNC
    '-o', '-'                 # Stream to stdout
]

# Use bufsize=0 for unbuffered, real-time data flow
pipe = subprocess.Popen(rpicam_cmd, stdout=subprocess.PIPE, bufsize=0)

# --- 3. VARIABLES & HUD ---
frame_count = 0
process_every_n_frames = 2 
threat_detected = False
current_action = "IDLE"
raw_buffer = b""

print("\n>>> SYSTEM LIVE: WAITING FOR SENSOR WARMUP... <<<")

try:
    while True:
        # Read from the pipe in smaller chunks to avoid blocking
        chunk = pipe.stdout.read(8192)
        if not chunk:
            continue
        raw_buffer += chunk
        
        # We need to find the start (0xffd8) and end (0xffd9) of a JPEG frame
        a = raw_buffer.find(b'\xff\xd8')
        b = raw_buffer.find(b'\xff\xd9')
        
        if a != -1 and b != -1 and a < b:
            jpg = raw_buffer[a:b+2]
            raw_buffer = raw_buffer[b+2:]
            
            # Decode the JPEG to an OpenCV image
            frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
            
            if frame is not None:
                frame_count += 1
                
                # --- AI INFERENCE (Every N frames) ---
                if frame_count % process_every_n_frames == 0:
                    # Resize to 320x240 inside the loop for AI speed
                    small_frame = cv2.resize(frame, (320, 240))
                    results = model(small_frame, stream=True, verbose=False)
                    
                    threat_detected = False
                    for r in results:
                        if any(model.names[int(box.cls[0])] == 'person' for box in r.boxes):
                            threat_detected = True
                
                # --- DRAWING THE HUD ---
                display_frame = frame.copy()
                cv2.rectangle(display_frame, (0, 0), (280, 80), (0, 0, 0), -1)
                cv2.putText(display_frame, f"ACT: {current_action}", (10, 30), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                
                if threat_detected:
                    if pico: pico.write(b's') # Emergency Stop
                    current_action = "AUTO-BRAKE"
                    cv2.putText(display_frame, "HUMAN DETECTED", (10, 65), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

                # SHOW VIDEO
                cv2.imshow("Rover Tactical Feed", display_frame)

            # --- KEYBOARD CONTROLS ---
            key = cv2.waitKey(1) & 0xFF
            if key == 27: # ESC
                break
            
            if not threat_detected and pico:
                if key == ord('w'): 
                    pico.write(b'f'); current_action = "FORWARD"
                elif key == ord('s'): 
                    pico.write(b'b'); current_action = "BACKWARD"
                elif key == ord('a'): 
                    pico.write(b'l'); current_action = "LEFT"
                elif key == ord('d'): 
                    pico.write(b'r'); current_action = "RIGHT"
                elif key == ord('q'): 
                    pico.write(b's'); current_action = "STOP"

finally:
    print("\nShutting down...")
    if pico: pico.write(b's')
    pipe.terminate()
    cv2.destroyAllWindows()
