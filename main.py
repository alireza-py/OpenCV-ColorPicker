import cv2
import numpy
from detecting import TheBall, Control, Frame

cap_object = cv2.VideoCapture(0)
ball = TheBall()

def main():
    while True:
        _, Frame.main = cap_object.read()
        ball.the_trackbar_hsv()
        result = ball.get_posation_with_hsv(Frame.main)
        print(result)
        if Control.DEBUG.value:
            result = ball.configs_key_control()
            if result == -1:
                break
    cv2.destroyAllWindows()
    cap_object.release()
if __name__ == '__main__':
    main()