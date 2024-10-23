from SettingsManager import Settings
from FolderManager import FolderManager
from UserInteraction import UserInterface
from CameraManager import PhotoManager
from PhotoTailor import Tailor

import utils
import os

class Runner:

    def __init__(self):
        self._settings = Settings()
        self._folders = FolderManager(self._settings.get_main_folder_path())
        self._ui = UserInterface()
        self._camera = PhotoManager()
        self._editor = Tailor()
        self._continue = True

    def prepare(self):
        print('ciao') # self._camera.start_camera()

    def start_new_session(self, photos_number):
        # variable "photos_number" contains the number of photos the user wants to make
        if photos_number != 0:
            if len(os.listdir(self._folders.get_current_path())) != 0:
                print("Please pay attention. There are photos you need to see")
                return True
                # aggiungiere il codice che porta poi successivamente a visualizzare l'elenco delle foto
            else:
                with open(os.path.join(self._settings.get_main_folder_path(), "session.txt"), "r") as session_file:
                    session_number = int(session_file.read()) + 1
                print(f"Session photo number is {session_number}")
                session_number = utils.get_string_from_session_number(session_number)
                for i in range(1, photos_number + 1):
                    target = self._camera.get_shoot_from_pc(self._folders.get_current_path(), self._ui, session_number, utils.get_string_from_photo_number(i))
                return True
        else:
            if len(os.listdir(self._folders.get_current_path())) != 0:
                print("There are precedent photos you need to see")
                return True
            else:
                print("Please pay attention. There aren't photos you need to see")
                return False

    def add_another_burst(self, choice):
        photo_number = list(os.listdir(os.path.join(self._folders.get_current_path())))[-1] # to make sure the names of photos in order to take the right number to continue the acquisition
        photo_number = photo_number.split('_')[-1]
        photo_number = int(photo_number.split('.')[0])
        with open(os.path.join(self._settings.get_main_folder_path(), "session.txt"), "r") as session_file:
            session_number = int(session_file.read()) + 1
        session_number = utils.get_string_from_session_number(session_number)
        for i in range(1, choice + 1):
            target = self._camera.get_shoot_from_pc(self._folders.get_current_path(), self._ui, session_number, utils.get_string_from_photo_number(photo_number + i))



        '''if 1 <= photos_number <= 5:
        if len(os.listdir(os.path.join(self._settings.get_main_folder_path(), 'current'))) is 0:
            return int(os.listdir(os.path.join(self._settings.get_main_folder_path(), 'originals'))[-1].split('_')[-1]) + 1
        else:
            print('hello world')'''

    def main_execution(self):
        while True:
            self._camera.get_shoot_from_pc(self._folders.get_current_path(), self._ui)
            photo_path, photo_name = utils.get_the_file_in_dir(self._folders.get_current_path())
            if self._ui.confirm_shot(photo_path, utils.detect_os()):
                # the photo is accepted, we can go on
                break

        effect_name = self._ui.choose_polaroid_effect()
        effect_path = utils.get_asset_path_from_name(effect_name)
        # let's edit it
        self._editor.set_infos(photo_path, effect_path, self._folders.get_output_folder_path())
        self._editor.edit(photo_name, self._folders.get_originals_path())

    def keep_going(self):
        # here in the future a more complex solution
        return self._continue

    def final_cleaning(self):
        self._camera.stop_camera()