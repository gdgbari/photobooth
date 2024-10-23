import shutil

from SettingsManager import Settings
from FolderManager import FolderManager
from CameraManager import PhotoManager
from UserInteraction import UserInterface
from PhotoTailor import Tailor

import utils
import os

from Runner import Runner

def main():
    print('hello world')

    settings = Settings()
    folders = FolderManager(settings.get_main_folder_path())
    user_interface = UserInterface()

    camera = PhotoManager()
    editor = Tailor()

    # CAMERA
    # end

    # here the photo is in the 'current' folder
    # let's ask the user it is the photo he likes
    photo_path, name = utils.get_the_file_in_dir(folders.get_current_path())
    user_interface.confirm_shot(photo_path, utils.detect_os())
    effect_name = user_interface.choose_polaroid_effect()
    effect_path = utils.get_asset_path_from_name(effect_name)
    # let's edit it
    editor.set_infos(photo_path, effect_path, folders.get_output_folder_path())
    editor.edit(name, folders.get_originals_path())

def new_main():
    ui = UserInterface()
    settings = Settings()
    folders = FolderManager(settings.get_main_folder_path())

    camera = PhotoManager()
    editor = Tailor()

    runner = Runner()
    runner.prepare()

    while True:
        choice = ui.show_initial_menu()

        if choice == 1:
            photos_number = ui.show_new_session_menu()
            result = runner.start_new_session(photos_number)

            if result:
                while True:
                    result_2 = ui.visualize_current_photos(folders.get_current_path())
                    if result_2 == "burst":
                        while True:
                            print("How many photos do you want to add?")
                            choice_2 = int(input("Enter your choice (press 6 if you want to come back): "))
                            if 1 <= choice_2 <= 5:
                                runner.add_another_burst(choice_2)
                            if choice_2 == 6:
                                    break

                            print("Please enter a valid choice")

                    if result_2 != "burst" and result_2 != "go back":
                        """photo_number = result_2.split('/')[-1]
                        photo_number = photo_number.split('_')[-1]
                        photo_number = int(photo_number.split('.')[0])
                        with open(os.path.join(settings.get_main_folder_path(), "session.txt"), "r") as session_file:
                            session_number = int(session_file.read()) + 1
                        session_number = utils.get_string_from_session_number(session_number)"""
                        photo_name = result_2.split('/')[-1]

                        effect_name = ui.choose_polaroid_effect()
                        effect_path = utils.get_asset_path_from_name(effect_name)
                        editor.set_infos(result_2, effect_path, folders.get_output_folder_path())
                        editor.edit(photo_name, folders.get_originals_path())

                        op_sys = utils.detect_os()
                        result = ui.confirm_shot(os.path.join(folders.get_output_folder_path(), photo_name), op_sys)

                        if result:
                            with open(os.path.join(settings.get_main_folder_path(), "session.txt"), "r") as session_file:
                                session_number = int(session_file.read()) + 1
                            session_number = utils.get_string_from_session_number(session_number)

                            os.mkdir(os.path.join(folders.get_originals_path(), session_number))

                            current_photos = os.listdir(folders.get_current_path())

                            for file_name in current_photos:
                                # Builing of starting path and arriving path of files
                                starting_path = os.path.join(folders.get_current_path(), file_name)
                                arriving_path = os.path.join(os.path.join(folders.get_originals_path(), session_number), file_name)

                                shutil.move(starting_path, arriving_path)

                            original_photos = os.listdir(folders.get_originals_path())

                            for file_name in original_photos:
                                if os.path.isfile(os.path.join(folders.get_originals_path(), file_name)):
                                    starting_path = os.path.join(folders.get_originals_path(), file_name)
                                    arriving_path = os.path.join(os.path.join(folders.get_originals_path(), session_number), file_name)

                                    shutil.move(starting_path, arriving_path)

                            photo_name_edited = photo_name.split('.')[0] + "_edited.jpg"
                            os.rename(os.path.join(folders.get_output_folder_path(), photo_name), os.path.join(folders.get_output_folder_path(), photo_name_edited))

                            with open(os.path.join(settings.get_main_folder_path(), "session.txt"), "w") as session_file:
                                session_file.write(session_number)

                            break
                        else:
                            shutil.move(os.path.join(folders.get_originals_path(), photo_name), os.path.join(folders.get_current_path(), photo_name))
                            os.remove(os.path.join(folders.get_output_folder_path(), photo_name))
                    else:
                        break

            # maybe there's the need to add an else here
        elif choice == 2:
            break
        #new_session_number = runner.start_new_session()
        #runner.main_execution()

if __name__ == '__main__':
    new_main()

