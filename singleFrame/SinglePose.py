import cv2
import mediapipe as mp
import math
import numpy as np
import threading
import logging
logging.basicConfig(level=logging.DEBUG)

import sys
sys.stdout.reconfigure(line_buffering=True)

pose_detector_lock = threading.Lock()
_detector = None

#################### basic function ########################

def get_pose_detector():
    global _detector
    if _detector is None:
        mp_pose = mp.solutions.pose
        _detector = mp_pose.Pose(static_image_mode=False)
    return _detector

def close_pose_detector():
    global _detector
    if _detector:
        _detector.close()
        _detector = None


#################### utils function ########################

# 사용자 포즈 추출 (정규화 포함)
def extract_pose_keypoints(frame):
    detector = get_pose_detector()
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    with pose_detector_lock:
        results = detector.process(image_rgb)

    if not results.pose_landmarks:
        return None

    landmarks = results.pose_landmarks.landmark
    indices = {
        "left_shoulder": 11, "right_shoulder": 12, "left_elbow": 13, "right_elbow": 14,
        "left_wrist": 15, "right_wrist": 16, "left_hip": 23, "right_hip": 24,
        "left_knee": 25, "right_knee": 26, "left_ankle": 27, "right_ankle": 28
    }
    extracted = {name: landmarks[idx] for name, idx in indices.items()}
    return normalize_pose_keypoints(extracted)

# 두 점 간 벡터 계산
def get_vector(a, b):
    return np.array([
        b['x'] - a['x'],
        b['y'] - a['y'],
        b['z'] - a['z']
    ])


# 벡터 간 코사인 유사도
def cosine_similarity(vec1, vec2):
    dot = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return (dot / (norm1 * norm2)) * 100.0


# 정규화 함수 (안무가/사용자 공통 적용 가능)
def normalize_pose_keypoints(extracted):
    base_x = (extracted["left_hip"].x + extracted["right_hip"].x) / 2
    base_y = (extracted["left_hip"].y + extracted["right_hip"].y) / 2
    norm_sq = sum((v.x - base_x) ** 2 + (v.y - base_y) ** 2 + v.z ** 2 for v in extracted.values())
    l2 = math.sqrt(norm_sq) or 1.0
    normalized = {
        name: {"x": (v.x - base_x) / l2, "y": (v.y - base_y) / l2, "z": v.z / l2}
        for name, v in extracted.items()
    }
    normalized["mid_hip"] = {"x": 0.0, "y": 0.0, "z": 0.0}
    return normalized



# 방향 및 포즈 정확도 비교
def compare_pose_bdp(user, ref):

    if user is None or ref is None:
        return 0.0
    
    
    # 비교할 부위별 관절쌍 정의
    body_vectors = {
        'left_upper_arm':    ("left_shoulder", "left_elbow"),
        'left_lower_arm':    ("left_elbow", "left_wrist"),
        'right_upper_arm':   ("right_shoulder", "right_elbow"),
        'right_lower_arm':   ("right_elbow", "right_wrist"),
        'left_upper_leg':    ("left_hip", "left_knee"),
        'left_lower_leg':    ("left_knee", "left_ankle"),
        'right_upper_leg':   ("right_hip", "right_knee"),
        'right_lower_leg':   ("right_knee", "right_ankle"),
    }

    weights = {
        'left_upper_arm': 1.0,
        'left_lower_arm': 1.0,
        'right_upper_arm': 1.0,
        'right_lower_arm': 1.0,
        'left_upper_leg': 1.0,
        'left_lower_leg': 1.0,
        'right_upper_leg': 1.0,
        'right_lower_leg': 1.0,
        'direction': 2.0
    }

    total_score = 0.0
    total_weight = 0.0

    # 허용 오차 및 감점 완화
    clip_threshold = 5.0
    tolerance_scale = 2.0

    def process_diff(diff):
        return max(0, (diff - clip_threshold) / tolerance_scale)
    

    for part, (j1, j2) in body_vectors.items():
        try:
            user_vec = get_vector(user[j1], user[j2])
            ref_vec = get_vector(ref[j1], ref[j2])
            part_score = cosine_similarity(user_vec, ref_vec)
        except Exception:
            part_score = 0.0  # 관절 누락 시 0점 처리

        total_score += weights[part] * part_score
        total_weight += weights[part]


     # 몸통 방향 점수 계산
    try:
        dx_user = user['right_shoulder']['x'] - user['left_shoulder']['x']
        dy_user = user['right_shoulder']['y'] - user['left_shoulder']['y']
        user_angle = math.degrees(math.atan2(dy_user, dx_user))

        dx_ref = ref['right_shoulder']['x'] - ref['left_shoulder']['x']
        dy_ref = ref['right_shoulder']['y'] - ref['left_shoulder']['y']
        ref_angle = math.degrees(math.atan2(dy_ref, dx_ref))

        diff_angle = ((user_angle - ref_angle + 180) % 360) - 180
        direction_score = max(0, 100 - process_diff(abs(diff_angle)))
    except Exception:
        direction_score = 0.0

    total_score += weights['direction'] * direction_score
    total_weight += weights['direction']


    # 디버깅 출력
    logging.debug(f"direction: {direction_score:.2f}")

    return round(total_score / total_weight, 2) if total_weight > 0 else 0.0
