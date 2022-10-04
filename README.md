# Macro Recorder

The best and most accurate macro recorder for Windows.\
Easy to use and open source.

### Record
```python
from macro_recorder import Recorder

my_recorder = Recorder()
my_recorder.record()

my_recorder.save("my_macro.json")
```

### Run
```python
from macro_recorder import Recorder

my_recorder = Recorder()
my_recorder.load("my_macro.json")

my_recorder.play(speed_factor=1.5, only_essential_moves=False)
```