import os
import yaml
import utils
from SettingsManager import Settings
import shutil

# FOLDERS EXPLANATION
#
#    main_folder
#       |___________> current       [ here the current shots: in future the user would choose from different shots]
#       |___________> originals     [ all the originals chosen shots                                              ]
#       |___________> output        [ all the outputs: cropped and cornered                                       ]
#

class FolderManager:

    def __init__(self, main_folder_path: str):

        self._main_folder_path = main_folder_path
        # now the paths of all the sub-folders
        self._current_folder_path = os.path.join(main_folder_path,'current')
        self._originals_folder_path = os.path.join(main_folder_path,'originals')
        self._output_folder_path = os.path.join(main_folder_path,'output')

        # then we check the folders consistency
        self._folder_consistency_assurance()

    def _folder_consistency_assurance(self):
        # if the sub-folders misses, will be created
        folder_list = [self._main_folder_path, self._current_folder_path,
                       self._originals_folder_path, self._output_folder_path]
        for folder in folder_list:
            if not os.path.exists(folder):
                os.makedirs(folder)
                os.chmod(folder, 0o777)

    def _temp_data_consistency_assurance(self):
        if not os.path.exists(os.path.join(self._main_folder_path, "temp_data.yaml")):
            data = {
                "session": 0
            }
            with open(os.path.join(self._main_folder_path, "temp_data.yaml")) as yaml_file:
                yaml.dump(data, yaml_file)

    def get_current_path(self) -> str:
        return self._current_folder_path

    def get_originals_path(self) -> str:
        return self._originals_folder_path

    def get_output_folder_path(self) -> str:
        return self._output_folder_path

    def get_current_folder_length(self) -> int:
        return len(os.listdir(self._current_folder_path))

    def clean_current_path(self, final_path, photo_name) -> str:
        """
        Move all the file from the current folder to the output folder but saves the new path of the chosen shoot
        :param chosen_photo_path: it's the old path of the photo which we will hold
        :return: the new path of the pointed photo
        """
        new_photo_path = ''

        for filename in os.listdir(self._current_folder_path):

            original_file_complete_path = os.path.join(self._current_folder_path, filename)
            destination_path = os.path.join(final_path, filename)

            shutil.move(original_file_complete_path, destination_path)

            """if original_file_complete_path == chosen_photo_path:
                new_photo_path = destination_path"""

        original_photos = os.listdir(self._originals_folder_path)

        for file_name in original_photos:  # for-cycle that moves the files in "originals" folder in the subfolder corresponding to the current session
            if os.path.isfile(os.path.join(self._originals_folder_path, file_name)):
                starting_path = os.path.join(self._originals_folder_path, file_name)
                arriving_path = os.path.join(final_path, file_name)

                shutil.move(starting_path, arriving_path)

        photo_name_edited = photo_name.split('.')[0] + "_edited.jpg"
        os.rename(os.path.join(self._output_folder_path, photo_name), os.path.join(self._output_folder_path, photo_name_edited))

        return os.path.join(self._output_folder_path, photo_name_edited)

class FileNaming:

    def __init__(self):
        self._temp_data_path = "./temp_data.yaml"
        self._settings = Settings()
        self._folder = FolderManager(self._settings.get_main_folder_path())

    def get_session_number(self) -> str:
        with open(self._temp_data_path, 'r') as yaml_file:
            yaml_dict = yaml.safe_load(yaml_file)

        return utils.get_string_from_session_number(yaml_dict["session"])

    def get_photo_name(self) -> str:
        with open(self._temp_data_path, 'r') as yaml_file:
            yaml_dict = yaml.safe_load(yaml_file)

        session_number = utils.get_string_from_session_number(yaml_dict["session"] + 1)
        photo_number = utils.get_string_from_photo_number(self._folder.get_current_folder_length() + 1)

        return f"DEVFESTBA24_{session_number}_{photo_number}.jpg"

    def increment_session_number(self) -> str:
        with open(self._temp_data_path, 'r') as yaml_file:
            yaml_dict = yaml.safe_load(yaml_file)

        yaml_dict["session"] = yaml_dict["session"] + 1

        with open(self._temp_data_path, 'w') as f:
            yaml.dump(yaml_dict, f, default_flow_style=False, allow_unicode=True)

        return utils.get_string_from_session_number(yaml_dict["session"])

    # DEBUG
    # file_naming = FileNaming()
    # print(file_naming.increment_session_number())