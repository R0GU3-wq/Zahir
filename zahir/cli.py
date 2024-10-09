#!/usr/bin/env python3

import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, Toplevel, Label
from zahir import combine_and_export_data, recover_deleted_files_from_usb, collect_and_analyze_logs, reconstruct_user_activity
import os
import subprocess

class ZahirApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Set the window title and size
        self.title("Zahir - Forensic Artifact Extraction Tool")
        self.geometry("600x500")

        # Set the background color to black
        self.configure(bg="black")

        # Call method to create widgets
        self.create_widgets()

    def create_widgets(self):
        # Modern styled header with larger text
        header = tk.Label(self, text="ZAHIR", font=("Helvetica", 70, "bold"), fg="lime", bg="black")
        header.pack(pady=(30, 10))

        # Subtitle
        subtitle = tk.Label(self, text="Forensic Artifact Extraction Tool", font=("Helvetica", 14), fg="lime", bg="black")
        subtitle.pack(pady=10)

        # Action selection label
        action_label = tk.Label(self, text="Choose an Action", font=("Helvetica", 16, "bold"), fg="lime", bg="black")
        action_label.pack(pady=20)

        button_style = {"bg": "black", "fg": "lime", "font": ("Arial", 12), "activebackground": "lime", "activeforeground": "black"}

        # Action buttons
        tk.Button(self, text="Extract Browser History", command=self.extract_browser_history, width=30, **button_style).pack(pady=5)
        tk.Button(self, text="Recover Deleted Files", command=self.recover_deleted_files, width=30, **button_style).pack(pady=5)
        tk.Button(self, text="Analyze Logs", command=self.analyze_logs, width=30, **button_style).pack(pady=5)
        tk.Button(self, text="Reconstruct User Activity", command=self.reconstruct_user_activity, width=30, **button_style).pack(pady=5)

    def themed_messagebox(self, title, message, box_type="info"):
        """
        Creates a custom messagebox styled with neon green text and black background
        """
        top = Toplevel(self)
        top.title(title)
        top.configure(bg="black")
        top.geometry("400x150")

        # Message content in neon green text
        msg = Label(top, text=message, font=("Arial", 12), fg="lime", bg="black", wraplength=350)
        msg.pack(pady=20)

        if box_type == "info":
            tk.Button(top, text="OK", command=top.destroy, **{"bg": "black", "fg": "lime"}).pack()
        elif box_type == "error":
            tk.Button(top, text="Close", command=top.destroy, **{"bg": "red", "fg": "black"}).pack()

        return top

    def extract_browser_history(self):
        # Custom instructions dialog
        instructions = """
        Please select the Firefox profile directory.
        On Linux, the profile is typically located at:
        /home/<username>/.mozilla/firefox/<profile folder>
        """
        msg_box = self.themed_messagebox("Information", instructions)
        self.wait_window(msg_box)  # Wait until the messagebox is closed

        firefox_profile = filedialog.askdirectory(title="Select Firefox Profile Directory")
        output_dir = filedialog.askdirectory(title="Select Output Directory for Extracted Data")
        if firefox_profile and output_dir:
            try:
                if not os.path.exists(firefox_profile):
                    raise FileNotFoundError(f"Directory not found: {firefox_profile}")
                
                combine_and_export_data(firefox_profile, output_dir)
                self.themed_messagebox("Success", f"Browser history extracted successfully and saved to {output_dir}/firefox_artifacts.xlsx.")
            except Exception as e:
                self.themed_messagebox("Error", f"Failed to extract browser history: {e}", box_type="error")

    def recover_deleted_files(self):
        msg_box = self.themed_messagebox("Information", "Please select the mount point and output directory.")
        self.wait_window(msg_box)  # Wait until the messagebox is closed

        mount_point = filedialog.askdirectory(title="Select Mount Point of Partition")
        output_dir = filedialog.askdirectory(title="Select Output Directory")

        if mount_point and output_dir:
           # Use simpledialog.askstring instead of filedialog.askstring
           device = simpledialog.askstring("Input", "Please enter the device path (e.g., /dev/sdb1):")
        
           if device:
              try:
                  # Ensure the device and output directory are valid and run the recovery process
                  recover_deleted_files_from_usb(mount_point, output_dir, device)
                  self.themed_messagebox("Success", f"Deleted files recovered. Output saved to {output_dir}.")
              except subprocess.CalledProcessError as e:
                  self.themed_messagebox("Error", f"Error during recovery: {e}", box_type="error")
              except Exception as e:
                  self.themed_messagebox("Error", f"Failed to recover deleted files: {e}", box_type="error")
           else:
              self.themed_messagebox("Error", "No device path provided.", box_type="error")
        else:
           self.themed_messagebox("Error", "Mount point or output directory not selected.", box_type="error")


    def analyze_logs(self):
        msg_box = self.themed_messagebox("Information", "Please select the output directory for the logs.")
        self.wait_window(msg_box)  # Wait until the messagebox is closed

        output_dir = filedialog.askdirectory(title="Select Output Directory for Logs")
        if output_dir:
            try:
                collect_and_analyze_logs(output_dir)
                self.themed_messagebox("Success", f"Logs analyzed. Output saved to {output_dir}.")
            except Exception as e:
                self.themed_messagebox("Error", f"Failed to analyze logs: {e}", box_type="error")

    def reconstruct_user_activity(self):
        msg_box = self.themed_messagebox("Information", "Please enter the username for reconstructing activity.")
        self.wait_window(msg_box)  # Wait until the messagebox is closed

        username = simpledialog.askstring("Input", "Enter the username for which you want to reconstruct activity:", parent=self)

        if not username:
            self.themed_messagebox("Error", "Username cannot be empty.", box_type="error")
            return

        output_dir = filedialog.askdirectory(title="Select Output Directory for User Activity")

        if output_dir:
            try:
                reconstruct_user_activity(output_dir, username)
                self.themed_messagebox("Success", f"User activity reconstructed for {username}. Output saved to {output_dir}.")
            except Exception as e:
                self.themed_messagebox("Error", f"Failed to reconstruct user activity for {username}: {e}", box_type="error")

if __name__ == '__main__':
    app = ZahirApp()
    app.mainloop()
