from macro_recorder import Recorder




if __name__ == '__main__':
    recorder = Recorder()
    # recorder.record()
    # recorder.save('test.json')
    #
    # time.sleep(1)

    recorder.load('test.json')
    recorder.play(speed_factor=2, only_essential_moves=False)

    # recorder.load('recorded.json')
    #

