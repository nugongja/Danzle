import cv2
import mediapipe as mp
import json
import math
import csv
import numpy as np
from tqdm import tqdm
from collections import deque
import sys
import os
import logging
logging.basicConfig(level=logging.DEBUG)

# 경로 설정
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'doubleFrame')))
from doublePose import extract_pose_keypoints, compare_pose_bdp, compare_pose_bdp_double_frame

# 기준 포즈 불러오기
with open('D:\\LearningPython\\capston\\originalKeypoints\\test_ref_pose_normalized.json', 'r') as f:
    ref_data = json.load(f)
ref_pose_by_frame = {int(frame): keypoints for frame, keypoints in ref_data.items()}

# 비디오 설정
user_path = 'D:\\LearningPython\\capston\\sampleVideos\\testUser.mp4'
cap = cv2.VideoCapture(user_path)
fps = cap.get(cv2.CAP_PROP_FPS)

# MediaPipe 초기화
mp_pose = mp.solutions.pose
frame_id = 0
cnt = 0
score_log = []

# 사용자/전문가 큐
user_pose_queue = deque(maxlen=2)
ref_pose_queue = deque(maxlen=2)

with mp_pose.Pose(static_image_mode=True) as pose:
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    pbar = tqdm(total=total_frames)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 필요 시 회전 보정
        #frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = pose.process(rgb)

        # 0.5초마다 점수 계산
        if frame_id % int(fps/2) == 0:
            logging.debug(f"frame_id: {cnt}")
            if cnt in ref_pose_by_frame:
                user_pose = extract_pose_keypoints(frame)
                ref_pose = ref_pose_by_frame[cnt]

                user_pose_queue.append(user_pose)
                ref_pose_queue.append(ref_pose)

                cnt += 1

                if len(user_pose_queue) == 2 and len(ref_pose_queue) == 2:
                    user_prev, user_now = user_pose_queue
                    ref_prev, ref_now = ref_pose_queue
                    score = compare_pose_bdp_double_frame(user_now, user_prev, ref_now, ref_prev)
                    score_log.append((frame_id // fps, score))
                else:
                    # 처음 프레임은 single frame 방식으로 평가
                    score = compare_pose_bdp(user_pose, ref_pose)

        frame_id += 1
        pbar.update(1)

cap.release()
pbar.close()

# ───────────────────────
# 점수 저장 및 통계
output_csv_path = "D:/LearningPython/capston/outputLogs/doublePose_scores.csv"
os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)

with open(output_csv_path, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["sec", "score"])
    for sec, score in score_log:
        writer.writerow([sec, score])

scores_only = [score for _, score in score_log]
if scores_only:
    mean_score = np.mean(scores_only)
    std_score = np.std(scores_only)
    print(f"\n✅ 평균 점수: {mean_score:.2f}")
    print(f"✅ 표준편차: {std_score:.2f}")
else:
    print("⚠️ 저장된 점수가 없습니다.")
