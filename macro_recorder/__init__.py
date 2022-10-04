import time, json, keyboard, mouse
from macro_recorder.thread import thread
from threading import Thread


class Recorder:

    def __init__(self, recorded: dict = None, stop_key: str = 'esc'):
        self.start_time = None
        self.stop_recording_flag = False
        self.play_start_time = None
        self.is_playing = False
        self.speed_factor = 1
        self.stop_key = stop_key

        self.recorded = recorded if recorded else {
            'keyboard': [],
            'mouse': []
        }

    def record(self, countdown: float = 0.001):
        self.start_time = time.time() + countdown
        self.mouse_listener()
        self.keyboard_listener()

    def play(self, countdown: float = 0.001, speed_factor: float = 1, only_essential_moves: bool = False):
        self.is_playing = True

        if speed_factor > 5:
            speed_factor = 5

        if only_essential_moves:
            self.filter_moves()

        self.speed_factor = speed_factor
        self.play_start_time = time.time() + countdown

        mouse_ = Thread(target=self.play_mouse, args=(self.recorded['mouse'],))
        keyboard_ = Thread(target=self.play_keyboard, args=(self.recorded['keyboard'],))
        self.stop_player()

        mouse_.start()
        keyboard_.start()
        mouse_.join()
        keyboard_.join()

        self.is_playing = False

    def save(self, path: str):
        with open(path, 'w') as f:
            json.dump(self.recorded, f, indent=4)

    def load(self, path: str):
        with open(path, 'r') as f:
            self.recorded = json.load(f)

    def keyboard_listener(self):
        self.wait_to_start(self.start_time)

        while True:
            event: keyboard.KeyboardEvent = keyboard.read_event()

            if self.stop_recording_flag:
                break

            if event.name == self.stop_key:
                self.stop_recording()
                break

            self.recorded['keyboard'].append([event.event_type == 'down', event.name, event.time - self.start_time])

    @thread
    def mouse_listener(self):
        self.wait_to_start(self.start_time)
        mouse.hook(self.on_callback)

    def on_callback(self, event):
        if isinstance(event, mouse.MoveEvent):
            self.recorded['mouse'].append(['move', event.x, event.y, event.time - self.start_time])

        elif isinstance(event, mouse.ButtonEvent):
            self.recorded['mouse'].append(['click', event.button, event.event_type == 'down', event.time - self.start_time])

        elif isinstance(event, mouse.WheelEvent):
            self.recorded['mouse'].append(['scroll', event.delta, event.time - self.start_time])

        else:
            print('Unknown event:', event)

    def stop_recording(self):
        mouse.unhook(self.on_callback)
        self.stop_recording_flag = True

        time.sleep(0.1)

        return self.recorded

    def play_keyboard(self, key_events: list):
        self.wait_to_start(self.play_start_time)

        for key in key_events:
            pressed, scan_code, t = key
            self.sleep(t / self.speed_factor)

            if not self.is_playing:
                break

            if pressed:
                keyboard.press(scan_code)

            else:
                keyboard.release(scan_code)

    def play_mouse(self, mouse_events: list):
        self.wait_to_start(self.play_start_time)

        for mouse_event in mouse_events:
            event_type, *args, t = mouse_event
            self.sleep(t / self.speed_factor)

            if not self.is_playing:
                break

            if event_type == 'move':
                mouse.move(*args)

            elif event_type == 'click':
                if args[1]:
                    mouse.press(args[0])

                else:
                    mouse.release(args[0])

            elif event_type == 'scroll':
                mouse.wheel(args[0])

    @staticmethod
    def wait_to_start(t: float):
        time_to_sleep = t - time.time()

        if time_to_sleep > 0:
            time.sleep(time_to_sleep)

    def sleep(self, t: float):
        time_to_sleep = t - (time.time() - self.play_start_time)

        if time_to_sleep > 0:
            time.sleep(time_to_sleep)

    @thread
    def stop_player(self):
        keyboard.wait(self.stop_key)
        print('Stopping player...')

        if self.is_playing:
            self.is_playing = False

    def filter_moves(self):
        filtered_moves = []
        last_event = None

        for i in range(len(self.recorded['mouse'])):
            current_event = self.recorded['mouse'][i]

            if current_event[0] != 'move':
                if last_event and last_event[0] == 'move':
                    filtered_moves.append(last_event)

                filtered_moves.append(current_event)
                
            last_event = current_event

        self.recorded['mouse'] = filtered_moves
