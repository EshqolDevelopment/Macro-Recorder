from macro_recorder import Recorder




if __name__ == '__main__':
    recorder = Recorder()
    recorder.record()
    recorder.save('recording.json')
    recorder.play()
