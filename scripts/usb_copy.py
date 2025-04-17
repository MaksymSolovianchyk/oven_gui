import pyudev
import shutil
import os
import time
import subprocess
from screens import settings_screen
def safe_eject_usb(device_node):
    """
    Unmounts and ejects a USB device safely.
    """
    try:
        # Unmount the device
        subprocess.run(['umount', device_node], check=True)
        print(f"Unmounted {device_node}")

        # Power off the USB device (if supported)
        subprocess.run(['udisksctl', 'power-off', '-b', device_node], check=True)
        print(f"Safely ejected {device_node}")
        settings_screen.Instructions="Presets added, you can remove the flash drive"
    except subprocess.CalledProcessError as e:
        print(f"Failed to eject {device_node}: {e}")

def copy_usb_content(target_dir):
    """
    Detects connected USB drives, copies their contents to target_dir.
    Overwrites existing files/folders. Ejects device after completion.
    """
    context = pyudev.Context()

    print("Scanning for USB devices...")

    for device in context.list_devices(subsystem='block', DEVTYPE='partition'):
        if device.get('ID_BUS') == 'usb':
            device_node = device.device_node
            print(f"Found USB device: {device_node}")

            # Check if it's mounted
            mount_path = None
            with open("/proc/mounts", "r") as mounts:
                for line in mounts:
                    if device_node in line:
                        mount_path = line.split()[1]
                        break

            if mount_path:
                print(f"Device mounted at: {mount_path}")

                label = device.get('ID_FS_LABEL') or "USB_Drive"
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                dest_dir = os.path.join(target_dir, f"{label}_{timestamp}")
                os.makedirs(dest_dir, exist_ok=True)

                print(f"Copying contents to {dest_dir}...")

                try:
                    for item in os.listdir(mount_path):
                        s = os.path.join(mount_path, item)
                        d = os.path.join(dest_dir, item)

                        if os.path.isdir(s):
                            if os.path.exists(d):
                                shutil.rmtree(d)
                            shutil.copytree(s, d)
                        else:
                            shutil.copy2(s, d)

                    print("Copy complete.")

                except Exception as e:
                    print(f"Error copying files: {e}")

                # Eject the device after copying
                safe_eject_usb(device_node)

            else:
                print("Device is not mounted.")

    print("USB scan finished.")
