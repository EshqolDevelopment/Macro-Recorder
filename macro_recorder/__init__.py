import time, json, keyboard, mouse
from macro_recorder.thread import thread
from threading import Thread


class Recorder:

    def __init__(self, recorded: dict = None, round_to: int = 5):
        self.start_time = None
        self.stop = False
        self.play_start_time = None
        self.round_to = round_to
        self.is_playing = False
        self.speed_factor = 1

        self.recorded = recorded if recorded else {
            'keyboard': [],
            'mouse': []
        }

    def record(self, countdown: float = 0.01, stop_key: str = 'esc'):
        self.start_time = time.time() + countdown
        self.mouse_listener()
        self.keyboard_listener(stop_key=stop_key)

    def play(self, countdown: float = 0.3, speed_factor: float = 1):
        threads = [
            Thread(target=self.play_mouse, args=(self.recorded['mouse'],)),
            Thread(target=self.play_keyboard, args=(self.recorded['keyboard'],))
        ]

        self.is_playing = True
        self.speed_factor = speed_factor
        self.play_start_time = time.time() + countdown

        for t in threads:
            t.start()

        for t in threads:
            t.join()

        self.is_playing = False

    def save(self, path: str):
        with open(path, 'w') as f:
            json.dump(self.recorded, f, indent=4)

    def load(self, path: str):
        with open(path, 'r') as f:
            self.recorded = json.load(f)

    def keyboard_listener(self, stop_key: str):
        while True:
            event: keyboard.KeyboardEvent = keyboard.read_event()

            if self.stop:
                break

            if event.name == stop_key:
                self.stop_recording()
                break

            self.recorded['keyboard'].append(
                [event.event_type == 'down', event.scan_code, event.time - self.start_time])

    @thread
    def mouse_listener(self):
        mouse.hook(self.on_callback)

    def on_callback(self, event):
        if isinstance(event, mouse.MoveEvent):
            self.recorded['mouse'].append(['move', event.x, event.y, event.time - self.start_time])

        elif isinstance(event, mouse.ButtonEvent):
            self.recorded['mouse'].append(
                ['click', event.button, event.event_type == 'down', event.time - self.start_time])

        elif isinstance(event, mouse.WheelEvent):
            self.recorded['mouse'].append(['scroll', event.delta, event.time - self.start_time])

        else:
            print('Unknown event:', event)

    def stop_recording(self):
        mouse.unhook(self.on_callback)
        self.stop = True

        time.sleep(0.1)

        return self.recorded

    def play_keyboard(self, key_events: list):
        self.wait_to_start()

        for key in key_events:
            pressed, scan_code, t = key
            self.sleep(t / self.speed_factor)

            if pressed:
                keyboard.send(scan_code, do_press=pressed, do_release=not pressed)

    def play_mouse(self, mouse_events: list):
        self.wait_to_start()

        for mouse_event in mouse_events:
            event_type, *args, t = mouse_event
            self.sleep(t / self.speed_factor)

            if event_type == 'move':
                mouse.move(*args)

            elif event_type == 'click':
                if args[1]:
                    mouse.press(args[0])

                else:
                    mouse.release(args[0])

            elif event_type == 'scroll':
                mouse.wheel(args[0])

    def wait_to_start(self):
        while time.time() < self.play_start_time:
            pass

    def sleep(self, t: float):
        while time.time() - self.play_start_time < t:
            time.sleep(0)



