from PIL import Image

# I choose to use this functions in a class because then transitioning to a GUI will be easier

class UserInterface:

    def choose_polaroid_effect(self) -> str:
        effect_list = ['Gemini', 'Flutter', 'Android', 'Firebase', 'Kotlin', 'Angular',
                       'Cloud', 'Jetpack Compose', 'TensorFlow', 'ARCore']

        print('Choose which effect to apply')

        while True:
            index = 1
            for effect_name in effect_list:
                print(f'[{index}]: {effect_name}')
                index = index + 1

            chosen_edit = input('pick a number: ')
            if chosen_edit.isdigit():
                chosen_edit = int(chosen_edit)
                if 0 < chosen_edit <= 10:
                    print('alright')
                    break

            print('Some error occurred, please try again')

        file_name = 'Polaroid - ' + str(chosen_edit) + '.png'
        return file_name

    def confirm_shot(self, photo_path) -> bool:
        image = Image.open(photo_path)
        image.show()

        while True:
            print('Do you like it? y/n')

            decision = input('choose: ')

            if decision == 'y':
                return True
            elif decision == 'n':
                return False

            print('Some error occurred, please try again')

    def press_to_shot(self):
        input('press any key to shoot')

    def notify_shot_taken(self):
        print('shot taken')