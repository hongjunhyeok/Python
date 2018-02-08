import numpy as np
import cv2


def show_webcam(mirror=False):

    capture = cv2.VideoCapture(0)
    print ('image width %d'%capture.get(3))
    print ('image height %d'%capture.get(4))

    capture.set(3,320)
    capture.set(4,240)

    while(True):
        ret,frame=capture.read()

        cv2.imshow('frame',frame)
        if cv2.waitKey(1)&0xFF ==ord('q'):
            break

    capture.release()
    cv2.destroyAllWindows()

def main():
    show_webcam(mirror=True)

if __name__=='__main__':
    main()