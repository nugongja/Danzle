import cv2
import mediapipe as mp
import json
import math
import time
from tqdm import tqdm
from collections import deque
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'doubleFrame')))
from doublePose import extract_pose_keypoints, compare_pose_bdp, compare_pose_bdp_double_frame

# 기준 포즈 불러오기
with open('D:\\LearningPython\\capston\\originalKeypoints\\test_ref_pose_normalized.json', 'r') as f:
    ref_data = json.load(f)

ref_pose_by_frame = {int(frame): keypoints for frame, keypoints in ref_data.items()}

# 사용자 영상 분석
user_path = 'D:\\LearningPython\\capston\\sampleVideos\\testUser.mp4'
cap = cv2.VideoCapture(user_path)
fps = cap.get(cv2.CAP_PROP_FPS)

# 첫 프레임을 읽어서 회전 후 해상도 확인
ret, sample_frame = cap.read()
if not ret:
    raise RuntimeError("비디오를 열 수 없습니다.")
#rotated_sample = cv2.rotate(sample_frame, cv2.ROTATE_90_CLOCKWISE)
height, width = sample_frame.shape[:2]
cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # 프레임 초기화

mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils
frame_id = 0
score = None
score_log = []

# 비디오 저장 설정 (회전 후 해상도)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('D:/LearningPython/capston/outputVideos/output_double.mp4', fourcc, fps, (width, height))

# 사용자/전문가 큐
user_pose_queue = deque(maxlen=2)
ref_pose_queue = deque(maxlen=2)

def compare_user_and_ref_pose(user_pose, ref_pose, frame_index=None):
    print(f"\n🔍 Comparing poses{f' at frame {frame_index}' if frame_index is not None else ''}")
    print("-" * 80)
    print(f"{'Joint':15s} | {'User (x, y, z)':30s} | {'Ref (x, y, z)':30s} | Diff")
    print("-" * 80)

    for joint in user_pose:
        if joint not in ref_pose:
            print(f"{joint:15s} | MISSING in ref_pose")
            continue

        u = user_pose[joint]
        r = ref_pose[joint]

        dx = abs(u['x'] - r['x'])
        dy = abs(u['y'] - r['y'])
        dz = abs(u['z'] - r['z'])
        total_diff = math.sqrt(dx**2 + dy**2 + dz**2)

        print(f"{joint:15s} | ({u['x']:.5f}, {u['y']:.5f}, {u['z']:.5f}) | "
              f"({r['x']:.5f}, {r['y']:.5f}, {r['z']:.5f}) | {total_diff:.5f}")



with mp_pose.Pose(static_image_mode=True) as pose:
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    pbar = tqdm(total=total_frames)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 90도 회전 보정
        #frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = pose.process(rgb)

        # 1초마다 점수 계산
        if frame_id % int(fps/2) == 0:
            if frame_id in ref_pose_by_frame:
                user_pose = extract_pose_keypoints(frame)
                ref_pose = ref_pose_by_frame[frame_id]

                compare_user_and_ref_pose(user_pose, ref_pose, frame_id)

                user_pose_queue.append(user_pose)
                ref_pose_queue.append(ref_pose)

                if len(user_pose_queue) == 2 and len(ref_pose_queue) == 2:
                    user_prev, user_now = user_pose_queue
                    ref_prev, ref_now = ref_pose_queue
                    score = compare_pose_bdp_double_frame(user_now, user_prev, ref_now, ref_prev)
                    score_log.append((frame_id // fps, score))
                    cv2.putText(frame, f'Score: {score}', (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
                else:
                    # 처음 프레임은 single frame 방식으로 평가
                    score = compare_pose_bdp(user_pose, ref_pose)


        # 점수는 매 프레임 출력
        if score is not None:
            cv2.putText(frame, f'Score: {score}', (30, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
        out.write(frame)  # 결과 프레임 저장
        frame_id += 1
        pbar.update(1)

pbar.close()
cap.release()
out.release() 
