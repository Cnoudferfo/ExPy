import time
print("Forever loop, press ctrl + c to stop")
try:
    while True:
        time.sleep(0.5)
except KeyboardInterrupt:
    pass
finally:
    print("Stopped!")