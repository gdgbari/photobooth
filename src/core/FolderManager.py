from src.settings.SettingsManager import Settings
from logging import DEBUG
import os
import shutil
import src.utils.utils as utils
import yaml


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

    def get_current_path(self) -> str:
        return self._current_folder_path

    def get_originals_path(self) -> str:
        return self._originals_folder_path

    def get_output_folder_path(self) -> str:
        return self._output_folder_path

    def clean_current_path(self, chosen_photo_path: str)->str:
        """
        Move all the file from the current folder to the originals folder but saves the new path of the chosen shoot
        :param chosen_photo_path: it's the old path of the photo which we will hold
        :return: the new path of the pointed photo
        """
        new_photo_path = ''

        for filename in os.listdir(self._current_folder_path):

            original_file_complete_path = os.path.join(self._current_folder_path, filename)
            destination_path = os.path.join(self._originals_folder_path, filename)
            shutil.move(original_file_complete_path, destination_path)

            if original_file_complete_path == chosen_photo_path:
                new_photo_path = destination_path

        return new_photo_path

class FileNaming:

    def __init__(self):
        self._temp_data_path = "temp_data.yaml"
        self._settings = Settings()

    def get_photo_name(self) -> str:
        with open(self._temp_data_path, 'r') as yaml_file:
            yaml_dict = yaml.safe_load(yaml_file)

        session_number = yaml_dict["session"]

        folder = FolderManager(self._settings.get_main_folder_path())
        photo_number = utils.get_string_from_photo_number(len(os.listdir(folder.get_current_path())) + 1)

        return f"DEVFESTBA_{utils.get_string_from_session_number(int(session_number) + 1)}_{photo_number}.jpg"

    def increment_session_number(self):
        with open(self._temp_data_path, 'r') as yaml_file:
            yaml_dict = yaml.safe_load(yaml_file)

        yaml_dict["session"] = utils.get_string_from_session_number(int(yaml_dict["session"]) + 1)

        with open(self._temp_data_path, 'w') as f:
            yaml.dump(yaml_dict, f, default_flow_style=False, allow_unicode=True)

        return yaml_dict["session"]

class AssetManager:

    def __init__(self):
        self.assets_path = str(os.path.join(os.getcwd(), "Assets"))

    def is_frame_single(self) -> bool:
        # check if the assets folder contains only one frame
        # if so, then we can skip the user choice
        if len(os.listdir(self.assets_path)) == 1:
            return True
        else:
            return False    
        
    def get_corners_names(self) -> list:
        # get the names of the corners
        corner_list = []
        for filename in os.listdir(self.assets_path):
            if filename.endswith(".png"):
                filename = filename.replace(".png", "")
                corner_list.append(filename)
        return corner_list

#DEBUG
# file_naming = FileNaming()
# print(file_naming.increment_session_number())
# asset_manager = AssetManager()
# print(asset_manager.get_corners_names())
