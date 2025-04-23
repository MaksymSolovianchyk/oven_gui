import pyudev
import shutil
import os
import time
import subprocess
from screens import settings_screen
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

def safe_eject_usb(device_node):
    try:
        subprocess.run(['umount', device_node], check=True)
        subprocess.run(['udisksctl', 'power-off', '-b', device_node], check=True)
        print(f"Safely ejected {device_node}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to eject {device_node}: {e}")

def mount_usb(device_node, mount_path='/mnt/usb'):
    os.makedirs(mount_path, exist_ok=True)
    try:
        subprocess.run(['mount', device_node, mount_path], check=True)
        print(f"Mounted {device_node} at {mount_path}")
        return mount_path
    except subprocess.CalledProcessError as e:
        print(f"Mounting failed: {e}")
        return None

def show_confirmation_popup(message="USB processed successfully!"):
    layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
    label = Label(text=message, size_hint=(1, 0.6))
    button = Button(text="OK", size_hint=(1, 0.4))

    popup = Popup(title='Operation Complete',
                  content=layout,
                  size_hint=(0.6, 0.4),
                  auto_dismiss=False)

    button.bind(on_press=popup.dismiss)
    layout.add_widget(label)
    layout.add_widget(button)

    popup.open()

def copy_usb_file(target_dir, filename="presets.xlsx"):
    context = pyudev.Context()
    print("Scanning for USB devices...")

    for device in context.list_devices(subsystem='block', DEVTYPE='partition'):
        if device.get('ID_BUS') == 'usb':
            device_node = device.device_node
            print(f"Found USB device: {device_node}")

            # Check if mounted
            mount_path = None
            with open("/proc/mounts", "r") as mounts:
                for line in mounts:
                    if device_node in line:
                        mount_path = line.split()[1]
                        break

            # Mount manually if needed
            if not mount_path:
                mount_path = mount_usb(device_node)

            if mount_path:
                source_file = os.path.join(mount_path, filename)
                dest_file = os.path.join(target_dir, filename)

                try:
                    if os.path.exists(source_file):
                        shutil.copy2(source_file, dest_file)
                        print(f"Copied {filename} to {target_dir}")
                        success = True
                    else:
                        print(f"{filename} not found on USB.")
                        success = False
                except Exception as e:
                    print(f"Error copying file: {e}")
                    success = False

                safe_eject_usb(device_node)

                # Show confirmation popup
                if success:
                    show_confirmation_popup("File copied & USB ejected!")
                else:
                    show_confirmation_popup("File not found or error during copy.")

            else:
                print("Device could not be mounted.")
                show_confirmation_popup("Could not mount USB drive.")

    print("Done.")