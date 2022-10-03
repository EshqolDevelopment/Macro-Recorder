from macro_recorder import Recorder




if __name__ == '__main__':


    recorder = Recorder()
    recorder.record(length=3)


    recorder.play(countdown=1)

    recorder.save('recording.json')



