import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner


class MyGridLayout(GridLayout):
    # Initialize infinite keywords
    def __init__(self, **kwargs):
        # Call grid layout constructor
        super(MyGridLayout, self).__init__(**kwargs)

        # Set columns
        self.cols = 1

        # Create a second gridlayout
        self.top_grid = GridLayout()
        # Set number of columns in our new top_grid
        self.top_grid.cols = 2

        # Add widgets
        self.top_grid.add_widget(Label(text="Area: "))
        # Add Input Box
        self.area = TextInput(multiline=True)
        self.top_grid.add_widget(self.area)

        self.top_grid.add_widget(Label(text="Rooms: "))
        # Add Input Box
        self.rooms = Spinner(text='Rooms',
                             values=('1', '2', '3', '4', '5'))
        self.top_grid.add_widget(self.rooms)

        self.top_grid.add_widget(Label(text="Floor: "))
        # Add Input Box
        self.floor = Spinner(text='Floors',
                             values=('1', '2', '3', '4', '5','6', '7', '8', '9', '10'))
        self.top_grid.add_widget(self.floor)

        # Add the new top_grid to our app
        self.add_widget(self.top_grid)

        # Create a Submit Button
        self.submit = Button(text="Get price", font_size=32)
        # Bind the button
        self.submit.bind(on_press=self.get_price)
        self.add_widget(self.submit)

    def get_price(self, instance):
        area = int(self.area.text)
        rooms = int(self.rooms.text)
        floor = int(self.floor.text)

        # print(f'Your area is {area} m, you have {rooms} rooms, and your floor is{floor}!')
        # Print it to the screen
        self.add_widget(Label(text=f'Your predicted price is {950 * area +  50 * (rooms * floor)}$!'))

        # Clear the input boxes
        self.area.text = ""
        self.rooms.text = ""
        self.floor.text = ""


class MyApp(App):
    def build(self):
        return MyGridLayout()


if __name__ == '__main__':
    MyApp().run()
