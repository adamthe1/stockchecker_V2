from threading import Thread
import winsound
from time import sleep


def main():
    frequency = 10000  # Set Frequency To 2500 Hertz
    duration = 5000  # Set Duration To 1000 ms == 1 second
    while True:
        t1 = Thread(target=playa())
        t2 = Thread(target=playc())
        t3 = Thread(target=playe())
        tr = [t1, t2, t3]

        for i in tr:
            i.start()
        sleep(1)
def playa():
    winsound.Beep(440, 1000)

def playc():
    winsound.Beep(523, 1000)

def playe():
    winsound.Beep(659, 1000)

if __name__ == '__main__':
    main()
