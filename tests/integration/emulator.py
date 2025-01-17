"""Main entrance point."""

from tkinter import (Tk,
                     Button,
                     Canvas,
                     Frame,
                     Label,
                     Scale,
                     StringVar,
                     LEFT,
                     VERTICAL)
from colorsys import hsv_to_rgb

from pico_copilot.utils.logger import LOG


class Emulator:
    """
    Test Emulator GUI.

    Usage:
        EMULATOR = Emulator()
        # blocking call:
        EMULATOR.display()
        # in a separate thread:
        EMULATOR.set_led_brightness(name, brightness)
    """

    MAX_BRIGHTNESS = 1.0
    DEFAULT_BRIGHTNESS = 0.5
    YELLOW_HSV_COLOR = [0.1667, 1, 1]
    GREEN_HSV_COLOR = [0.3333, 1, 1]
    RED_HSV_COLOR = [0, 1, 1]

    def __init__(self):
        """Init the window params."""
        self._root = None
        self._tail_light_frame = None
        self._front_light_frame = None

        self._window_width = 800
        self._window_height = 300
        self._bar_width = 30
        self._bar_height = self._window_height

        self._tail_light_width = self._window_width // 3
        self._tail_light_height = self._window_height
        self._front_light_width = self._window_width // 3
        self._front_light_height = self._window_height

        self._status_light_width = self._window_width // 6
        self._status_light_height = self._window_height

        self._button_width = self._window_width // 200
        self._button_height = self._window_height // 100
        self._button_pressed = False

        self._colors = {
            'tail': {
                'leds': {
                    'tail_1': '#000000',
                    'tail_2': '#000000',
                    'tail_3': '#000000',
                    'tail_4': '#000000',
                },
                'updated': True,
                'color': self.RED_HSV_COLOR,
            },
            'front': {
                'leds': {
                    'front_1': '#000000',
                    'front_2': '#000000',
                    'front_3': '#000000',
                    'front_4': '#000000',
                },
                'updated': True,
                'color': self.YELLOW_HSV_COLOR,
            },
            'status': {
                'leds': {
                    'status': '#000000',
                },
                'updated': True,
                'color': self.GREEN_HSV_COLOR,
            },
        }

        self._create_window()

    def display(self):
        """Display the main window. Blocking call."""
        self._root.mainloop()

    def set_led_brightness(self, name, brightness):
        """Set led brightness based on its name."""
        known_name = False
        # FIXME: simplify
        for led_group in ('tail', 'front', 'status'):
            if name in self._colors[led_group]['leds']:
                known_name = True
                self._colors[led_group]['leds'][name] = (
                    self._get_tinted_html_color(
                        self._colors[led_group]['color'],
                        brightness))
                # LOG.debug(f'{led_group} {name} was set to {brightness}')
                self._colors[led_group]['status'] = True
        if not known_name:
            LOG.warning('Unknown led name')

    def get_light_sensor(self):
        return float(self._light_scale_value.get())

    def get_button_state(self):
        return self._button_pressed

    def _create_window(self):
        """Create a window and frames."""
        self._root = Tk()

        self._create_elements()

        self._root.after(0, self._update_lights)

    def _get_tinted_html_color(self, base_hsv_color, brightness):
        hsv_color = base_hsv_color
        hsv_color[2] = brightness
        return '#' + ''.join(
            ['%02x' % round(i * 255) for i in hsv_to_rgb(*hsv_color)])

    def _update_lights(self):
        call_map = {
            'tail': self._draw_tail_light,
            'front': self._draw_front_light,
            'status': self._draw_status_light,
        }

        for led_group in ('tail', 'front', 'status'):
            if self._colors[led_group]['status']:
                call_map[led_group]()
                self._colors[led_group]['status'] = False

        self._root.after(100, self._update_lights)

    def _button_click(self, _event):
        # LOG.debug('Button click')
        self._button_pressed = True

    def _button_release(self, _event):
        # LOG.debug('Button release')
        self._button_pressed = False

    # Hardcoded drawing functions

    def _create_elements(self):
        """Create all elements like led stripes, buttons, etc."""
        self._tail_light_frame = Frame(master=self._root,
                                       width=self._window_width // 2,
                                       height=self._window_height,
                                       bg='grey')
        self._tail_light_frame.pack(padx=30, side=LEFT)
        self._add_label(self._tail_light_frame, 'Tail light')
        self._tail_light_canvas = Canvas(self._tail_light_frame,
                                         width=self._tail_light_width,
                                         height=self._tail_light_height)
        self._tail_light_canvas.pack()

        self._front_light_frame = Frame(master=self._root,
                                        width=self._window_width // 2,
                                        height=self._window_height,
                                        bg='grey')
        self._front_light_frame.pack(padx=30, side=LEFT)
        self._add_label(self._front_light_frame, 'Front light')
        self._front_light_canvas = Canvas(self._front_light_frame,
                                          width=self._front_light_width,
                                          height=self._front_light_height)
        self._front_light_canvas.pack()

        self._status_light_frame = Frame(master=self._root,
                                         width=self._window_width // 2,
                                         height=self._window_height,
                                         bg='grey')
        self._status_light_frame.pack(padx=30, side=LEFT)
        self._add_label(self._status_light_frame, 'Status light')
        self._status_light_canvas = Canvas(self._status_light_frame,
                                           width=self._status_light_width,
                                           height=self._status_light_height)
        self._status_light_canvas.pack()

        self._light_sensor_frame = Frame(master=self._root,
                                         width=self._window_width // 2,
                                         height=self._window_height,
                                         bg='grey')
        self._light_sensor_frame.pack(padx=30, side=LEFT)
        self._add_label(self._light_sensor_frame, 'Light sensor')

        self._light_scale_value = StringVar()
        self._light_sensor_scale = Scale(self._light_sensor_frame,
                                         variable=self._light_scale_value,
                                         from_=self.MAX_BRIGHTNESS,
                                         to=0.0,
                                         digits=2,
                                         resolution=0.1,
                                         orient=VERTICAL)
        self._light_sensor_scale.set(self.DEFAULT_BRIGHTNESS)
        self._light_sensor_scale.pack()

        self._button_frame = Frame(master=self._root,
                                   width=self._window_width // 2,
                                   height=self._window_height,
                                   bg='grey')
        self._button_frame.pack(padx=30, side=LEFT)
        self._add_label(self._button_frame, 'Button')
        self._button_element = Button(self._button_frame,
                                      width=self._button_width,
                                      height=self._button_height,
                                      bg='grey')
        self._button_element.bind("<ButtonPress>", self._button_click)
        self._button_element.bind("<ButtonRelease>", self._button_release)
        self._button_element.pack()

    def _add_label(self, parent, text):
        label = Label(parent, text=text)
        label.pack(fill='both')

    def _get_bar_rectangle(self, start_x, start_y):
        return (start_x,
                start_y,
                start_x + self._bar_width,
                start_y + self._bar_height)

    def _draw_front_light(self):
        self._front_light_canvas.create_rectangle(
            *self._get_bar_rectangle(0,
                                     0),
            outline='black',
            fill=self._colors['front']['leds']['front_1'])

        self._front_light_canvas.create_rectangle(
            *self._get_bar_rectangle(self._bar_width * 2,
                                     0),
            outline='black',
            fill=self._colors['front']['leds']['front_2'])

        self._front_light_canvas.create_rectangle(
            *self._get_bar_rectangle(self._bar_width * 4,
                                     0),
            outline='black',
            fill=self._colors['front']['leds']['front_3'])

        self._front_light_canvas.create_rectangle(
            *self._get_bar_rectangle(self._bar_width * 6,
                                     0),
            outline='black',
            fill=self._colors['front']['leds']['front_4'])

    def _draw_tail_light(self):
        self._tail_light_canvas.create_rectangle(
            *self._get_bar_rectangle(0,
                                     0),
            outline='black',
            fill=self._colors['tail']['leds']['tail_1'])

        self._tail_light_canvas.create_rectangle(
            *self._get_bar_rectangle(self._bar_width * 2,
                                     0),
            outline='black',
            fill=self._colors['tail']['leds']['tail_2'])

        self._tail_light_canvas.create_rectangle(
            *self._get_bar_rectangle(self._bar_width * 4,
                                     0),
            outline='black',
            fill=self._colors['tail']['leds']['tail_3'])

        self._tail_light_canvas.create_rectangle(
            *self._get_bar_rectangle(self._bar_width * 6,
                                     0),
            outline='black',
            fill=self._colors['tail']['leds']['tail_4'])

    def _draw_status_light(self):
        """Draw a status LED."""
        led_radius = self._status_light_width // 8
        led_x = self._status_light_width // 2
        led_y = self._status_light_height // 2

        self._status_light_canvas.create_oval(
            led_x - led_radius,
            led_y - led_radius,
            led_x + led_radius,
            led_y + led_radius,
            outline='black',
            fill=self._colors['status']['leds']['status'])


class BoardInterface:
    """Interface between an emulator window and a control module."""
    DEFAULT_BRIGHTNESS = 0.0

    def __init__(self, board, config):
        """Board initialization."""
        self._board = board
        for _set_name, set_params in config['leds'].items():
            for name, params in set_params['leds'].items():
                self._board.set_led_brightness(name, self.DEFAULT_BRIGHTNESS)

    def change_brightness(self, name, brightness):
        """Change brightness for a led element in the window."""
        # LOG.debug(f' Board IF: {name} brightness: {brightness}')
        self._board.set_led_brightness(name, brightness)

    def get_light_sensor(self):
        """Get the value of a light sensor slider in the window."""
        return self._board.get_light_sensor()

    def get_button_state(self):
        return self._board.get_button_state()
