# EnVi-Guard-Your-Friendly-Doorbell-Security-Camera
This is a Python-based smart security system that simulates a real-world doorbell camera system with owner-controlled access. Built using Tkinter and OpenCV, the system provides a simple yet functional simulation of a live home monitoring and door control interface, complete with timestamps and action logging.

📦 Install Requirements
pip install opencv-python
This library is for live camera streaming, the most important component of this project.

pip install pillow
This module is actually called Pillow, which is the modern fork of PIL (Python Imaging Library) and is actively maintained.

📌 Features
🎥 Live Camera Feed
Uses OpenCV to continuously display the camera feed.
Positioned at the top center of the interface.

🔔 Doorbell System
A “Ring Doorbell” button simulates a visitor pressing the bell.
Triggers the display of Accept and Reject buttons for owner action.

✅ Access Control
Accept Button: Unlocks the door and displays Door Unlocked.
Reject Button: Displays Access Denied for 10 seconds, then resets the status to Door Locked.

🔒 Manual Door Control
Lock Door button available at all times to manually lock the door after unlocking.

🕒 Date and Time Display
Real-time display of day, date (DD/MM/YYYY) and time (24-hour format) shown below the camera feed.
Mimics CCTV-style timestamping.

🛠️ Requirements
Python 3.7+
OpenCV
Tkinter (usually pre-installed with Python)
