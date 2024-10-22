# this class get the chosen photo and applies the wanted corner

from PIL import Image
import os
import shutil

class Tailor:

    def __init__(self):
        self._photo_path = ''
        self._effect_path = ''
        self._output_folder_path = ''

    def set_infos(self, first_photo: str, first_effect: str,second_photo: str, second_effect: str, output_folder_path: str):
        """
        Preliminary information for processing the single photo (it must be called before the editing of every photo).
        :param first_photo: the path as string of the chosen photo
        :param first_effect: the path as string of the chosen effect ( the polaroid file in /assets )
        :param output_folder_path: the path as string of the edited file
        """
        self._first_photo = first_photo
        self._first_effect = first_effect
        self._second_photo = second_photo
        self._second_effect = second_effect
        self._output_folder_path = output_folder_path

    def edit(self, edited_file_name: str)-> str:
        """
        Edits the photos
        :param edited_file_name: the name of the file (with extension!), it is not the path,
               it will be the name of the final file
        :return: the path, as string, of the edited file
        """
        # DISCUSSION ABOUT THE DIMENSION AND RATIO OF THE IMAGE
        #   analysis on the true height of the polaroid 41+760+10 = 810 -> the height of the background (760) is 93%
        #   true height of the polaroid is 2000 -> the height wanted of the background is 1860

        #   what about the margin? the left and right margin are of 41 px as the upper margin, 41 px is 5% of height
        #   which with our dimension translate to 100 px

        #   the data extrapolated before are from wrong measure
        #   it seems that the correct h of the input image is 1528 px or 76,4 %
        #   it seam that the correct upper margin is 83 px or 4,15 %
        # END OF DISCUSSION


        edited_file_path = os.path.join(self._output_folder_path,edited_file_name)
        first_photo = self._prepare_single_photo(self._first_photo,self._first_effect)
        second_photo = self._prepare_single_photo(self._second_photo,self._second_effect)
        output_file = self._combine_two_photos(first_photo,second_photo)

        output_file.save(edited_file_path, "JPEG")

        # give 777 to edited file
        os.chmod(edited_file_path, 0o777)

        # self._final_cleaning(originals_folder,edited_file_name)
        return edited_file_path

    def _combine_two_photos(self, first_photo: Image, second_photo: Image) -> Image:
        output_image = Image.new('RGB', size=(2000,1500)) # right now the output is rotated
        output_image.paste(first_photo, (0, 0))
        output_image.paste(second_photo, (750, 0))
        return output_image

    def _prepare_single_photo(self, photo, effect) -> Image:
        background = Image.open(photo)
        foreground = Image.open(effect)

        # transform the background in order to have a height of 1528 px, width of same ratio
        background_width, background_height = background.size
        new_background_height = 1528
        new_background_width = int((new_background_height / background_height) * background_width)
        background = background.resize((new_background_width, new_background_height), Image.Resampling.LANCZOS)
        background_width = new_background_width
        background_height = new_background_height

        # align the background width to the foreground width ( cutting the excess margin )
        foreground_width, foreground_height = foreground.size
        lateral_margin_to_cut = (background_width - foreground_width) // 2
        background = background.crop(
            (lateral_margin_to_cut, 0, lateral_margin_to_cut + foreground_width, background_height))

        # add padding space on the top and the bottom of the background image, to have the same height of foreground
        margin_space = 82
        new_background = Image.new('RGB', (foreground_width, foreground_height), 'black')
        new_background.paste(background, (0, margin_space))
        background = new_background

        # combine background and foreground
        background.paste(foreground, (0, 0), foreground)

        # now we want it in half h:2000 w:1500 -> h:1000 w:750
        output = background.resize((750,1000))

        return output


    # def _final_cleaning(self, originals_folder : str, file_name : str):
        # WARNING: this function is deprecated
        # at the end the file in the current folder has to be moved in the originals folder
        # previous_path = self._photo_path
        # final_path = os.path.join(originals_folder,file_name)
        # shutil.move(previous_path,final_path)


# DEBUG
# ph_path = "/home/gape01/PycharmProjects/photobooth/Assets/test.jpg"
# eff_path = "/home/gape01/PycharmProjects/photobooth/Assets/Polaroid - 1.png"
# output_f = "/home/gape01/Desktop"
# tailor = Tailor(ph_path,eff_path,output_f)
tailor = Tailor()
tailor.set_infos('/mnt/c/Users/gassi/Desktop/main/test.jpg',
                 '/mnt/c/Users/gassi/PycharmProjects/photobooth/Assets/Polaroid - 1.png',
                 '/mnt/c/Users/gassi/Desktop/main/test.jpg',
                 '/mnt/c/Users/gassi/PycharmProjects/photobooth/Assets/Polaroid - 1.png',
                 '/mnt/c/Users/gassi/Desktop/main/output')
tailor.edit("prova.jpg")