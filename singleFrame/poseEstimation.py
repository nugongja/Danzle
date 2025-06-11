import cv2
import mediapipe as mp
import json
import math
import time
from tqdm import tqdm
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'singleFrame')))
from SinglePose import extract_pose_keypoints, compare_pose_bdp

# 기준 포즈 불러오기
with open('D:\LearningPython\capston\originalKeypoints\SuperShy_ref_pose_filtered_1sec_normalized.json', 'r') as f:
    ref_data = json.load(f)

ref_pose_by_frame = {entry['frame']: entry['keypoints'] for entry in ref_data}

# ───────────────────────
# 사용자 영상 분석
user_path = 'D:/LearningPython/capston/sampleVideos/SuperShy.mp4'
cap = cv2.VideoCapture(user_path)
fps = cap.get(cv2.CAP_PROP_FPS)
fps = 30

# 첫 프레임을 읽어서 회전 후 해상도 확인
ret, sample_frame = cap.read()
if not ret:
    raise RuntimeError("비디오를 열 수 없습니다.")
rotated_sample = cv2.rotate(sample_frame, cv2.ROTATE_90_CLOCKWISE)
height, width = rotated_sample.shape[:2]
cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # 프레임 초기화

mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils

frame_id = 0
latest_score = None

# 비디오 저장 설정 (회전 후 해상도)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('D:/LearningPython/capston/outputVideos/output_single.mp4', fourcc, fps, (width, height))

with mp_pose.Pose() as pose:
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    pbar = tqdm(total=total_frames)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 90도 회전 보정
        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)


        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = pose.process(rgb)

        # 1초마다 점수 계산
        if frame_id % int(fps) == 0:
            if frame_id in ref_pose_by_frame:
                user_pose = extract_pose_keypoints(frame)
                ref_pose = ref_pose_by_frame[frame_id]
                latest_score = compare_pose_bdp(user_pose, ref_pose)
                cv2.putText(frame, f'Score: {latest_score}', (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

        # 점수는 매 프레임 출력
        if latest_score is not None:
            cv2.putText(frame, f'Score: {latest_score}', (30, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
        out.write(frame)  # 결과 프레임 저장
        frame_id += 1
        pbar.update(1)

pbar.close()
cap.release()
out.release() 
