import wmi
import os
import time
import shutil
c = wmi.WMI()

class Reader:
    check = True

    @staticmethod
    def create_folder(path):
        if not os.path.isdir(path):
            os.makedirs(path)

    @classmethod
    def wait_falsh(cls):
        for disk in c.Win32_LogicalDisk():
            if disk.Description == "Съемный диск":
                print(disk.DeviceID)
                cls.download_files(disk.DeviceID, disk.VolumeSerialNumber, disk.VolumeName)
    
    @classmethod
    def download_files(cls, disk_id, disk_number, disk_name):

        path = f"folder\{disk_name}_{disk_number}"
        cls.create_folder(path)
        dir = os.listdir(disk_id)
        for i in range(1, len(dir)):
            copy_path = f"{disk_id}\{dir[i]}"
            try:
                shutil.copy2(copy_path, path)
            except:
                new_path = f"{path}\{dir[i]}"
                cls.create_folder(new_path)
                cls.download_files(new_path, disk_number, disk_name)

def main():
    classobject = Reader()
    while classobject.check:
        classobject.wait_falsh()
        time.sleep(5)

if __name__ == "__main__":
    main()