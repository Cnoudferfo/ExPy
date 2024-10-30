import pyaudio
import wave
import sys
import os
import time

pa = pyaudio.PyAudio()

try:
    numHostApi = pa.get_host_api_count()
    print(f"host API count={numHostApi}")
    hostIndex = -1
    for i in range(numHostApi):
        info = pa.get_host_api_info_by_index(i)
        numdevices = info.get('deviceCount')
        deviceIndex = -1
        for j in range(numdevices):
            info = pa.get_device_info_by_host_api_device_index(i,j)
            if 'Logi USB' in info.get('name'):
                deviceIndex = j
                print(f"(i={i},j={j}),index={info['index']},name={info['name']},maxInCh={info['maxInputChannels']}")
                break
        if deviceIndex > -1:
            hostIndex = i
            break

    CHUNK = 1024
    SAMPLE_FORMAT = pyaudio.paInt16
    CHANNELS = 1
    FS = 44100
    SECONDS = 5

    frames = list()
    count = 0

    def callback(in_data, frame_count, time_info, flag):
        global count
        global frames
        frames.append(in_data)
        count += 1
        if count < 150:
            ret = pyaudio.paContinue
        else:
            ret = pyaudio.paAbort
        return (in_data, ret)
    n = 0
    if 1:
        stream = pa.open(format=SAMPLE_FORMAT,\
                        channels=CHANNELS,\
                        rate=FS,\
                        frames_per_buffer=CHUNK,\
                        input=True,\
                        input_device_index=deviceIndex,\
                        stream_callback= callback)
        while stream.is_active():
            time.sleep(1.0)
            n += 1
            if n > 15:
                break
    else:
        stream = pa.open(format=SAMPLE_FORMAT,\
                        channels=CHANNELS,\
                        rate=FS,\
                        frames_per_buffer=CHUNK,\
                        input=True,\
                        input_device_index=deviceIndex)

        print(f"Get ready to record...")
        time.sleep(2)
        print(f"Recording started.")
        for i in range(int((FS/CHUNK)*SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
        print(f"Recording stopped.")

    print(f"n={n}, len(frames)={len(frames)}")

    stream.stop_stream()
    stream.close()

    wf = wave.open('test.wav', 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(pa.get_sample_size(SAMPLE_FORMAT))
    wf.setframerate(FS)
    wf.writeframes(b''.join(frames))

except Exception as e:
    print(f"Error e={e}")
finally:
    wf.close()
    pa.terminate()