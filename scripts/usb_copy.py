import pyudev
import shutil
import os
import time

def copy_usb_content(target_dir):
    """
    Detects connected USB drives, copies their contents to target_dir.
    If a file or folder with the same name exists, it will be overwritten.
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

                # Copy contents to target_dir/device_label_timestamp
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
                            # If destination directory exists, remove it first
                            if os.path.exists(d):
                                shutil.rmtree(d)
                            shutil.copytree(s, d)
                        else:
                            # If destination file exists, overwrite it
                            shutil.copy2(s, d)

                    print("Copy complete.")
                except Exception as e:
                    print(f"Error copying files: {e}")
            else:
                print("Device is not mounted.")

    print("USB scan finished.")
