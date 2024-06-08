import traceback

from kivymd.app import MDApp
from kivymd.uix.label import MDLabel

from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen

from notification import AndroidNotification


class SearchScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # notify instance
        self.notification = AndroidNotification()

        # notification send button
        self.push_button = Button(
            text='Notificate',

            # make the invisible button
            # text='blob',
            # background_color=(0, 0, 0, 0),

            size_hint=(1, None),
            height="48dp",
            on_press=self.send_notification
        )

        # label indicates the status of the sent msg
        self.info_label = MDLabel(
            text="",
            halign="center",
            theme_text_color="Error",
            size_hint=(1, None),
            height="48dp"
        )

        # main vertical layout
        main_layout = BoxLayout(orientation="vertical", spacing="10dp", padding=[10, 50, 10, 10])

        # create a vertical box layout to hold button and label
        vertical_layout = BoxLayout(orientation="vertical", size_hint=(1, None), height="100dp")

        # create the anchor layout
        anchor_layout = AnchorLayout(anchor_x='center', anchor_y='top')

        # add button and label to the vertical layout
        vertical_layout.add_widget(self.push_button)
        vertical_layout.add_widget(self.info_label)

        # add the vertical layout to the anchor layout
        anchor_layout.add_widget(vertical_layout)

        main_layout.add_widget(anchor_layout)
        self.add_widget(main_layout)

    def send_notification(self, *args) -> None:
        """ Safety send notifications. Error label can be used as info or a debugging element.
        """
        try:
            self.notification.notify(
                title='Notification title',
                message='Notification message',
                ticker="Notification ticker",
                toast=False,
                # icon name in ./res/drawable folder
                app_icon="notif_icon.png"
            )
            self.info_label.text = 'Notification sent successfully.'
        except Exception as _:
            self.info_label.text = f'Notification error: {traceback.format_exc()}'


class MyApp(MDApp):
    def build(self):
        search_screen = SearchScreen(name="search_screen")
        return search_screen


if __name__ == "__main__":
    MyApp().run()
