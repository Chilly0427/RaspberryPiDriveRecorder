# Import Library
import cv2
import time

# Class
class DriveRecorder:
    def __init__(self):
        print("===== Drive Recoreder Constructor =====")

    def __del__(self):
        print("===== Drive Recoreder Destructor =====")

    def capture(self):
        print("===== Start Capture =====")
        capture = cv2.VideoCapture(0) # ビデオキャプチャ

        #fps = int(self.CAPTURE.get(cv2.CAP_PROP_FPS)) # カメラのfps
        fps = 10 # 処理が遅くならない時間
        window_width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        window_height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        window_size = (window_width, window_height)
        fmt = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        video_writer = cv2.VideoWriter('./video.mp4', fmt, fps, window_size)

        over_time = 0
        first_flg = True

        while(True):
            start = time.time()
            #print("Start Time : " + str(start))
            ret, frame = capture.read()
            if not ret:
                break

            frame = cv2.resize(frame, window_size)

            video_writer.write(frame)
            cv2.imshow('Drive Recorder', frame)

            end = time.time()
            #print("End Time : " + str(end))

            sleep_time = 1 / fps - (end - start) - over_time
            print("Sleep Time : " + str(sleep_time))

            if sleep_time < 0:
                if first_flg == True:
                    print("First")
                    first_flg = False
                else:
                    over_time = sleep_time
                    print("Over Time : " + str(over_time))
            else:
                over_time = 0
                time.sleep(sleep_time)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        video_writer.release()
        capture.release()
        cv2.destroyAllWindows()

# main()
dr = DriveRecorder()
dr.capture()

