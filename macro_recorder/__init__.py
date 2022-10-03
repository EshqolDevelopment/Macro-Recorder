from pynput.mouse import Controller, Listener, Button
from pynput.keyboard import Key, Controller as KeyboardController, Listener as KeyboardListener
import time, threading, json



class Recorder:

    def __init__(self, recorded: dict = None, round_to: int = 5):
        self.mouse = Controller()
        self.keyboard = KeyboardController()

        self.listener = Listener(on_click=self.on_click, on_move=self.on_move, on_scroll=self.on_scroll)
        self.keyboard_listener = KeyboardListener(on_press=lambda *args: self.on_press(*args), on_release=lambda *args: self.on_press(*args, press=False))

        self.start_time = None
        self.stop = False
        self.play_start_time = None
        self.round_to = round_to
        self.is_playing = False

        self.recorded = recorded if recorded else {
            'move': [],
            'click': [],
            'scroll': [],
            'keyboard': []
        }
        self.keyboard_to_run()

    def record(self, length: int = None):
        self.start_time = time.time()
        self.listener.start()
        self.keyboard_listener.start()

        if length:
            while time.time() - self.start_time < length:
                pass

            self.stop_recording()

    def play(self, wait: bool = True, countdown: float = 0.3):
        threads = [threading.Thread(target=self.play_moves, args=(self.recorded['move'],)),
                   threading.Thread(target=self.play_clicks, args=(self.recorded['click'],)),
                   threading.Thread(target=self.play_scrolls, args=(self.recorded['scroll'],)),
                   threading.Thread(target=self.play_keyboard, args=(self.recorded['keyboard'],))]

        self.is_playing = True
        self.play_start_time = time.time() + countdown

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        self.is_playing = False

        if wait:
            self.wait_while_playing()

    def save(self, path: str):
        with open(path, 'w') as f:
            self.keyboard_to_json()
            json.dump(self.recorded, f, indent=4)

    def load(self, path: str):
        with open(path, 'r') as f:
            self.recorded = json.load(f)
            self.keyboard_to_run()

    def keyboard_to_run(self):
        keyboard = self.recorded['keyboard']

        for i in range(len(keyboard)):
            key, pressed, t = keyboard[i]
            print(key)
            key = self.get_key(key)
            keyboard[i] = [key, pressed, t]

        self.recorded['keyboard'] = keyboard

    def keyboard_to_json(self):
        keyboard = self.recorded['keyboard']

        for i in range(len(keyboard)):
            key, pressed, t = keyboard[i]

            if hasattr(key, '_name_'):
                keyboard[i] = [key._name_, pressed, t]

            else:
                keyboard[i] = [key.char, pressed, t]

        self.recorded['keyboard'] = keyboard

    def wait_while_playing(self):
        while self.is_playing:
            time.sleep(0.03)

    def on_click(self, x, y, button: Button, pressed):
        self.recorded['click'].append([x, y, [button._value_, button._name_], pressed, time.time() - self.start_time])

    def on_move(self, x, y):
        self.recorded['move'].append([x, y, time.time() - self.start_time])

    def on_scroll(self, x, y, dx, dy):
        self.recorded['scroll'].append([x, y, dx, dy, time.time() - self.start_time])

    def on_press(self, key: Key, press: bool = True):
        self.recorded['keyboard'].append([key, press, time.time() - self.start_time])

    def stop_recording(self):
        self.listener.stop()
        self.keyboard_listener.stop()
        self.stop = True

        time.sleep(0.1)

        return self.recorded

    def play_moves(self, moves: list):
        self.wait_to_start()

        for move in moves:
            x, y, t = move
            while time.time() - self.play_start_time < t:
                pass

            self.mouse.position = (x, y)

    def play_clicks(self, clicks: list):
        self.wait_to_start()

        for click in clicks:
            x, y, button, pressed, t = click
            while time.time() - self.play_start_time < t:
                pass

            my_button = Button.left if button[1] == 'left' else Button.right

            if pressed:
                self.mouse.press(my_button)
            else:
                self.mouse.release(my_button)

    def play_scrolls(self, scrolls: list):
        self.wait_to_start()

        for scroll in scrolls:
            x, y, dx, dy, t = scroll
            while time.time() - self.play_start_time < t:
                pass

            self.mouse.scroll(dx, dy)
            
    def play_keyboard(self, keyboard: list):
        self.wait_to_start()

        for key in keyboard:
            key, pressed, t = key
            while time.time() - self.play_start_time < t:
                pass

            if pressed:
                self.keyboard.press(key)

            else:
                self.keyboard.release(key)

    @staticmethod
    def get_key(key: str):
        key = key.lower()
        key_map = {
            'ctrl': Key.ctrl,
            'alt': Key.alt,
            'shift': Key.shift,
            'esc': Key.esc,
            'enter': Key.enter,
            'backspace': Key.backspace,
            'tab': Key.tab,
            'caps_lock': Key.caps_lock,
            'space': Key.space,
            'page_up': Key.page_up,
            'page_down': Key.page_down,
            'end': Key.end,
            'home': Key.home,
            'left': Key.left,
            'up': Key.up,
            'right': Key.right,
            'down': Key.down,
            'delete': Key.delete,
            'cmd': Key.cmd,
            'cmd_r': Key.cmd_r,
            'f1': Key.f1,
            'f2': Key.f2,
            'f3': Key.f3,
            'f4': Key.f4,
            'f5': Key.f5,
            'f6': Key.f6,
            'f7': Key.f7,
            'f8': Key.f8,
            'f9': Key.f9,
            'f10': Key.f10,
            'f11': Key.f11,
            'f12': Key.f12,
            'f13': Key.f13,
            'f14': Key.f14,
            'f15': Key.f15,
            'f16': Key.f16,
            'f17': Key.f17,
            'f18': Key.f18,
            'f19': Key.f19,
            'f20': Key.f20,
        }

        try:
            return key_map[key]

        except KeyError:
            return key
    
    def wait_to_start(self):
        while time.time() < self.play_start_time:
            pass