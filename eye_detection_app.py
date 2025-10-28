import cv2
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import threading
import time

class EyeDetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Eye State Detection")
        self.root.geometry("800x600")
        
        # Initialize variables
        self.camera_active = False
        self.cap = None
        self.eye_state_buffer = []  # Buffer to smooth out detection
        self.buffer_size = 5  # Number of frames to average
        
        # Load Haar Cascade classifiers
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
        
        # Create UI
        self.create_ui()
        
    def create_ui(self):
        # Title label
        title_label = ttk.Label(self.root, text="Eye State Detection App", font=("Arial", 20, "bold"))
        title_label.pack(pady=10)
        
        # Video display frame
        self.video_frame = ttk.Label(self.root)
        self.video_frame.pack(pady=10)
        
        # Camera button
        self.camera_btn = ttk.Button(self.root, text="Open Camera", command=self.toggle_camera)
        self.camera_btn.pack(pady=10)
        
        # Status label
        self.status_label = ttk.Label(self.root, text="Camera is OFF", font=("Arial", 12))
        self.status_label.pack(pady=5)
        
    def toggle_camera(self):
        if not self.camera_active:
            self.start_camera()
        else:
            self.stop_camera()
    
    def start_camera(self):
        self.camera_active = True
        self.cap = cv2.VideoCapture(0)
        
        # Set camera properties for better performance
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        
        # Wait for camera to initialize
        time.sleep(0.5)
        
        self.camera_btn.config(text="Close Camera")
        self.status_label.config(text="Camera is ON - Detecting eyes...")
        
        # Clear buffer
        self.eye_state_buffer = []
        
        # Start video thread
        self.video_thread = threading.Thread(target=self.update_frame, daemon=True)
        self.video_thread.start()
    
    def stop_camera(self):
        self.camera_active = False
        if self.cap:
            self.cap.release()
        self.camera_btn.config(text="Open Camera")
        self.status_label.config(text="Camera is OFF")
        self.video_frame.config(image="")
    
    def detect_eye_state(self, frame):
        """Detect faces and eyes, and determine if eyes are open or closed"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Apply histogram equalization for better detection in various lighting
        gray = cv2.equalizeHist(gray)
        
        # Detect faces with adjusted parameters for stability
        faces = self.face_cascade.detectMultiScale(
            gray, 
            scaleFactor=1.1, 
            minNeighbors=5,
            minSize=(100, 100),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        
        for (x, y, w, h) in faces:
            # Draw rectangle around face
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            
            # Region of interest for eyes (upper 60% of face)
            eye_region_y = y + int(h * 0.15)
            eye_region_h = int(h * 0.45)
            roi_gray = gray[eye_region_y:eye_region_y+eye_region_h, x:x+w]
            roi_color = frame[eye_region_y:eye_region_y+eye_region_h, x:x+w]
            
            # Detect eyes with optimized parameters
            eyes = self.eye_cascade.detectMultiScale(
                roi_gray,
                scaleFactor=1.05,
                minNeighbors=8,
                minSize=(20, 20),
                maxSize=(80, 80)
            )
            
            # Filter and sort eyes by x-coordinate (left to right)
            if len(eyes) > 0:
                eyes = sorted(eyes, key=lambda e: e[0])
                # If more than 2 eyes detected, keep only the 2 most prominent
                if len(eyes) > 2:
                    eyes = sorted(eyes, key=lambda e: e[2] * e[3], reverse=True)[:2]
                    eyes = sorted(eyes, key=lambda e: e[0])
            
            # Add to buffer for smoothing
            self.eye_state_buffer.append(len(eyes))
            if len(self.eye_state_buffer) > self.buffer_size:
                self.eye_state_buffer.pop(0)
            
            # Get averaged eye count
            avg_eye_count = sum(self.eye_state_buffer) / len(self.eye_state_buffer)
            
            # Determine state based on averaged detection
            if avg_eye_count < 0.5:
                # Both eyes closed
                cv2.putText(frame, "Both Eyes: CLOSED", (x, y-10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            elif avg_eye_count < 1.5:
                # One eye open
                cv2.putText(frame, "One Eye Detected", (x, y-10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 165, 255), 2)
                if len(eyes) >= 1:
                    ex, ey, ew, eh = eyes[0]
                    cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)
                    eye_pos = "Left" if ex < w/2 else "Right"
                    cv2.putText(frame, f"{eye_pos} Eye: OPEN", (x+ex, eye_region_y+ey-10), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            else:
                # Both eyes open
                cv2.putText(frame, "Both Eyes: OPEN", (x, y-10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                
                # Label each eye
                for i, (ex, ey, ew, eh) in enumerate(eyes[:2]):
                    cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)
                    
                    # Determine left or right based on x position
                    eye_label = "Left Eye: OPEN" if ex < w/2 else "Right Eye: OPEN"
                    cv2.putText(frame, eye_label, (x+ex, eye_region_y+ey-10), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        return frame
    
    def update_frame(self):
        """Continuously update the video frame"""
        while self.camera_active:
            ret, frame = self.cap.read()
            if ret:
                # Flip frame horizontally for mirror effect
                frame = cv2.flip(frame, 1)
                
                # Detect eye state
                frame = self.detect_eye_state(frame)
                
                # Convert frame to ImageTk format
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame_rgb)
                img = img.resize((640, 480), Image.Resampling.LANCZOS)
                imgtk = ImageTk.PhotoImage(image=img)
                
                # Update the video frame
                self.video_frame.imgtk = imgtk
                self.video_frame.config(image=imgtk)
                
                # Small delay to prevent overwhelming the system
                time.sleep(0.03)  # ~30 FPS
            else:
                break
    
    def on_closing(self):
        """Handle window closing event"""
        self.stop_camera()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = EyeDetectionApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
