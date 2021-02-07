# Import Library
import cv2

# Class
class DriveRecorder:
    WINDOW_W = 800 # ウインドウ幅
    WINDOW_H = 600 # ウインドウ高さ
    CAPTURE = cv2.VideoCapture(0) # ビデオキャプチャ

    def __init__(self):
        print("===== Drive Recoreder Constructor =====")

    def __del__(self):
        print("===== Drive Recoreder Destructor =====")
        self.CAPTURE.release()
        cv2.destroyAllWindows()

    def capture(self):
        print("===== Start Capture =====")

        while(True):
            ret, frame = self.CAPTURE.read()
            # resize the window
            windowsize = (self.WINDOW_W, self.WINDOW_H)
            frame = cv2.resize(frame, windowsize)

            cv2.imshow('Drive Recorder',frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

# main()
dr = DriveRecorder()
dr.capture()

