# Import Library
import cv2
import datetime
import time
import os

# Const
#TIME_OF_REC_MIN = 1 # 1ファイルの時間(分)
TIME_OF_REC_MIN = 1/6 # 1ファイルの時間(分)
MAX_FILE_NUM = 5 # 最大ファイル数

DIR_NAME = "./Video/" # 動画保存用ディレクトリ名
BASE_FILE_NAME = "DriveRecorder" # ファイル名のベース
FILE_EXT = ".mp4" # ファイル拡張子
FILE_NAME = "NULL" # ファイル名

CAPTURE = cv2.VideoCapture(0) # ビデオキャプチャ

#FPS = int(self.CAPTURE.get(cv2.CAP_PROP_FPS)) # カメラのfps
FPS = 10 # 処理が遅くならない時間にする
WINDOW_W = int(CAPTURE.get(cv2.CAP_PROP_FRAME_WIDTH)) # ウインドウ幅
WINDOW_H = int(CAPTURE.get(cv2.CAP_PROP_FRAME_HEIGHT)) # ウインドウ高さ
WINDOW_SIZE = (WINDOW_W, WINDOW_H) # ウインドウサイズ(ウインドウ幅xウインドウ高さ)
FMT = cv2.VideoWriter_fourcc('m', 'p', '4', 'v') # 動画保存フォーマット

# Val
over_time = 0 # 処理が間に合わなかった時間(つじつま合わせで次の処理を早くするために使う)
rec_time = 0 # 録画時間
check_rec_time = 0 # REC_TIMEを合計して指定時間を超えたか確認する

first_flg = True # 初回かどうか
file_change_flg = True # ファイルを変更するかどうか

while(True): # 動画を取得し続ける
    rec_start = time.time() # 録画時間計測開始

    if file_change_flg == True: # 指定時間が経過しているか
        if not os.path.isdir(DIR_NAME): # 動画保存用のディレクトリが存在しているか
            os.mkdir(DIR_NAME) # ディレクトリを作成
        files = os.listdir(DIR_NAME) # ディレクトリのファイルリストを取得
        if len(files) >= MAX_FILE_NUM: # 指定ファイル数になったら
            files.sort() # ファイルリストを昇順に並び替え
            os.remove(DIR_NAME + files[0]) # 先頭のファイル=一番古いファイルを削除
        dt_now = datetime.datetime.now() # 現在の時刻を取得する
        dt_now_str = dt_now.strftime("%Y%m%d%H%M%S") # 現在の時刻をyyyymmddhhmmss形式に変換する
        FILE_NAME = DIR_NAME + str(dt_now_str) + "_" + BASE_FILE_NAME + FILE_EXT # 新しい動画のファイル名
        video_writer = cv2.VideoWriter(FILE_NAME, FMT, FPS, WINDOW_SIZE) # ビデオ書き込み用
        file_change_flg = False # ファイルの変更が終わったのでフラグを落とす

    ret, frame = CAPTURE.read() # カメラから1フレーム読み込む
    if not ret: # カメラから取得できなかった場合
        break # 終了する

    capture_start = time.time() # 1フレーム取得にかかる時間計測開始
    #print("Start Time : " + str(capture_start))

    frame = cv2.resize(frame, WINDOW_SIZE) # 取得したフレームをウインドウサイズに合わせる

    # ウインドウの最大化(ディスプレイ側)
    cv2.namedWindow('Drive Recorder', cv2.WINDOW_NORMAL)
    cv2.setWindowProperty('Drive Recorder', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    video_writer.write(frame) # 動画ファイルに書き出す
    cv2.imshow('Drive Recorder', frame) # ウインドウに表示する

    capture_end = time.time() # 1フレーム取得にかかる時間計測終了
    #print("End Time : " + str(capture_end))

    sleep_time = 1 / FPS - (capture_end - capture_start) - over_time # 現在のフレームレートに対して処理時間に余裕がある場合は待つ(待たないと動画が早送りになる)．また、前フレームで現在のフレームレートより時間がかかった場合は辻褄を合わせるために待ち時間を減らす
    #print("Sleep Time : " + str(sleep_time))

    if sleep_time < 0: # 待ち時間が負になる=現在のフレームレートに対して処理が間に合っていない
        if first_flg == True: # 初回はカメラ準備で時間がかかるため、待ち時間は計算対象外
            #print("First")
            first_flg = False # 初回が終わったらフラグを落とす
        else: # 2回目以降は処理時間をオーバーした時間を記録し、次のフレームで今回分の待ち時間を減らす
            over_time = sleep_time
            #print("Over Time : " + str(over_time))
    else: # 待ち時間が正の場合=現在のフレームレートに対して処理に余裕がある
        over_time = 0 # 処理に余裕があるのでオーバーした時間を0に戻す
        time.sleep(sleep_time) # 現在のフレームに対して早く処理が終わったのでその分待つ

    rec_end = time.time() # 録画時間計測終了
    rec_time = rec_end - rec_start # 今回のフレームでの処理時間を計算
    check_rec_time += rec_time # 前回までのフレームの処理時間を足す

    print("Check Rec Time : " + str(check_rec_time))
    if (check_rec_time / 60) > TIME_OF_REC_MIN: # 前回までのフレームの処理時間の合計が指定時間を超えた場合
        rec_time = 0 # 録画時間計測をリセット
        check_rec_time = 0 # 前回までのフレームの処理時間の合計をリセット
        file_change_flg = True # 新規ファイルを作成するためにファイル変更フラグを立てる

    if cv2.waitKey(1) & 0xFF == ord('q'): # "q"を押してソフトを終了させる
        break

# 後始末
video_writer.release()
CAPTURE.release()
cv2.destroyAllWindows()