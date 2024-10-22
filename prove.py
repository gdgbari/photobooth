import os
from SettingsManager import Settings

settings = Settings()

if not os.path.exists(settings.get_main_folder_path()):
    os.makedirs(settings.get_main_folder_path())
    os.makedirs(os.path.join(settings.get_main_folder_path(), "current"))
    os.makedirs(os.path.join(settings.get_main_folder_path(), "originals"))
    os.makedirs(os.path.join(settings.get_main_folder_path(), "output"))

# if len(os.listdir(os.path.join(settings.get_main_folder_path(), 'current'))) == 0:
    # print(int(os.listdir(os.path.join(settings.get_main_folder_path(), 'originals'))[-1].split('_')[-1]) + 1)

print(os.listdir('/mnt/c/Users/fcarn/Desktop/Projects/photobooth/Assets'))

for i in range(1,8):
    print(i)

photo_number = os.listdir(os.path.join(settings.get_main_folder_path(), "current"))[-1]
photo_number = photo_number.split('_')[-1]
photo_number = int(photo_number.split('.')[0])
print(photo_number)