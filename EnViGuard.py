import cv2
import threading
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from datetime import datetime
from date_time_widget import DateTimeWidget
#import time

# -------------------- Global Control Variables --------------------
door_locked = True          # Door starts locked
bell_pressed = False        # Becomes True when bell is pressed
button_timer = None         # To store timeout countdown thread

# -------------------- GUI Callback Functions --------------------

def ring_bell():
    """
    Called when the user presses the doorbell button.
    Shows Accept/Reject buttons and starts 30s timeout.
    """
    global bell_pressed, button_timer

    if bell_pressed:  # Avoid duplicate presses while timer is running
        return

    bell_pressed = True
    timestamp = datetime.now().strftime("[%A, %d/%m/%Y %H:%M:%S]")
    print(f"{timestamp} Someone rang your door bell")
    accept_button.pack(pady=5)
    reject_button.pack(pady=5)

    # Start a 30-second timeout
    button_timer = threading.Timer(30.0, timeout_decision)
    button_timer.start()

def timeout_decision():
    """
    Called if 30 seconds pass with no Accept/Reject response.
    Hides buttons and resets state.
    """
    global bell_pressed
    bell_pressed = False
    hide_decision_buttons()
    print("[Timeout] No response. Door remains locked.")
    door_status_var.set("🔒 Access Denied (No response)")
    # Revert to locked after 10 seconds
    root.after(10000, lambda: door_status_var.set("🔒 Door Locked"))

def accept():
    """
    Called when user presses 'Accept'. Unlocks the door.
    """
    global door_locked, bell_pressed

    if button_timer:
        button_timer.cancel()

    door_locked = False
    timestamp = datetime.now().strftime("[%A, %d/%m/%Y %H:%M:%S]")
    print(f"{timestamp} ✅ Door unlocked by owner.")
    messagebox.showinfo("Door Status", "Door Unlocked!")
    door_status_var.set("🔓 Door Unlocked")
    close_button.pack(pady=10)  # Show Close Door button
    reset_state()

def reject():
    """
    Called when user presses 'Reject'. Keeps the door locked.
    """
    global door_locked, bell_pressed

    if button_timer:
        button_timer.cancel()

    door_locked = True
    timestamp = datetime.now().strftime("[%A, %d/%m/%Y %H:%M:%S]")
    print(f"{timestamp} ❌ Door remains locked (rejected).")
    messagebox.showinfo("Door Status", "Access Denied.")
    door_status_var.set("🔒 Access Denied")
    # Revert to locked after 10 seconds
    root.after(10000, lambda: door_status_var.set("🔒 Door Locked"))
    reset_state()

def reset_state():
    """
    Resets system state after decision is made.
    """
    global bell_pressed
    bell_pressed = False
    hide_decision_buttons()

def hide_decision_buttons():
    """
    Removes Accept and Reject buttons from the GUI.
    """
    accept_button.pack_forget()
    reject_button.pack_forget()

def close_door():
    """
    Manually re-locks the door after it has been unlocked.
    """
    global door_locked
    door_locked = True
    door_status_var.set("🔒 Door Locked")
    timestamp = datetime.now().strftime("[%A, %d/%m/%Y %H:%M:%S]")
    print(f"{timestamp}🚪 Door manually closed and locked.")
    close_button.pack_forget()  # Hide the button after closing

# -------------------- Video Streaming Thread --------------------

def video_loop():
    """
    Captures video frames and updates the GUI canvas.
    """
    success, frame = cap.read()
    if success:
        # Convert BGR (OpenCV) to RGB (Tkinter)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        video_label.imgtk = imgtk  # Save reference to avoid garbage collection
        video_label.configure(image=imgtk)
    video_label.after(10, video_loop)  # Run every 10ms for smooth feed

# -------------------- Main Setup --------------------

# Initialize camera
cap = cv2.VideoCapture(0)

# Setup GUI window
root = tk.Tk()
root.title("Smart Doorbell Camera")
root.geometry("600x520")
root.configure(bg="#e0f7fa")

# Title label
tk.Label(root, text="🏠 Environment Vision Guard: Your Friendly Security System", font=("Helvetica", 10, "bold"), bg="#e0f7fa").pack(pady=10)

# Video label (for live camera feed)
# Main content frame (horizontal layout)
main_frame = tk.Frame(root, bg="#e0f7fa")
main_frame.pack(fill=tk.BOTH, expand=True)

# -------------------- LEFT SIDE: Video + Status --------------------

left_frame = tk.Frame(main_frame, bg="#e0f7fa")
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Video label (Live camera feed)
video_label = tk.Label(left_frame)
video_label.pack(pady=5)
datetime_widget = DateTimeWidget(left_frame)
datetime_widget.pack(pady=(0, 10))

# Door Status Label (below video)
door_status_var = tk.StringVar()
door_status_var.set("🔒 Door Locked")

status_label = tk.Label(left_frame, textvariable=door_status_var,
                        font=("Helvetica", 14, "bold"),
                        bg="#fff3e0", fg="#000000",
                        relief=tk.SUNKEN, bd=2, width=25, pady=5)
status_label.pack(pady=10)

# -------------------- RIGHT SIDE: Button Panel --------------------

right_frame = tk.Frame(main_frame, bg="#e0f7fa")
right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=20)

# Doorbell Button
bell_button = tk.Button(right_frame, text="🔔 Ring Doorbell",
                        font=("Helvetica", 14), bg="#81d4fa", width=20,
                        relief=tk.RAISED, bd=3, command=ring_bell)
bell_button.pack(pady=10)

# Accept / Reject Buttons (initially hidden)
accept_button = tk.Button(right_frame, text="✅ Accept",
                          font=("Helvetica", 14), bg="#a5d6a7", width=20,
                          relief=tk.RAISED, bd=3, command=accept)

reject_button = tk.Button(right_frame, text="❌ Reject",
                          font=("Helvetica", 14), bg="#ef9a9a", width=20,
                          relief=tk.RAISED, bd=3, command=reject)

# Close Door Button (initially hidden)
close_button = tk.Button(right_frame, text="🔒 Lock Door",
                         font=("Helvetica", 14), bg="#fbc02d", width=20,
                         relief=tk.RAISED, bd=3, command=close_door)


# Start video loop
video_loop()

# Run GUI
# -------------------- Cleanup on Close --------------------
def cleanup():
    """
    Properly closes the camera and GUI when window is closed.
    """
    if button_timer:  # Stop any running timer
        button_timer.cancel()
    if cap.isOpened():
        cap.release()
    root.destroy()
root.protocol("WM_DELETE_WINDOW", cleanup)
root.mainloop()