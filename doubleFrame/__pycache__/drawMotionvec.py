import cv2
import os
import numpy as np
import json
import logging

# 기존 핸들러 제거
for h in logging.root.handlers[:]:
    logging.root.removeHandler(h)

# 새 핸들러 등록
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

logging.debug("🔥 로그 출력 테스트")


def normalize_keys(pose_dict):
    return {k.lower(): v for k, v in pose_dict.items()}

# MediaPipe 스타일 기본 연결관계 (일반적인 2D 포즈 기준)
POSE_CONNECTIONS = [
    ("left_shoulder", "right_shoulder"),
    ("left_shoulder", "left_elbow"),
    ("left_elbow", "left_wrist"),
    ("right_shoulder", "right_elbow"),
    ("right_elbow", "right_wrist"),
    ("left_shoulder", "left_hip"),
    ("right_shoulder", "right_hip"),
    ("left_hip", "right_hip"),
    ("left_hip", "left_knee"),
    ("left_knee", "left_ankle"),
    ("right_hip", "right_knee"),
    ("right_knee", "right_ankle"),
]

def to_centered_pixel(p, w, h, scale=0.3):
    cx = int(w / 2 + p['x'] * w * scale)
    cy = int(h / 2 + p['y'] * h * scale)
    return cx, cy


def draw_pose(frame, pose_dict, color, w, h):
    def to_px(p):
        return to_centered_pixel(p, w, h, scale=0.3)  # ✅ 중앙 배치 적용

    for joint1, joint2 in POSE_CONNECTIONS:
        if joint1 in pose_dict and joint2 in pose_dict:
            pt1 = to_px(pose_dict[joint1])
            pt2 = to_px(pose_dict[joint2])
            cv2.line(frame, pt1, pt2, color, 1)

    for joint in pose_dict:
        pt = to_px(pose_dict[joint])
        cv2.circle(frame, pt, 2, color, -1)



def draw_skeletons_without_video(user_pose_dict, ref_pose_dict, output_path, w=720, h=1280, fps=30):
    cv2.namedWindow('Pose Only', cv2.WINDOW_NORMAL)
    w, h = 720, 1280  # 원하는 해상도 지정
    fps = 2  # 영상 저장용 프레임 속도 (예: 초당 2프레임)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (w, h))

    # ✅ 포즈 데이터에 있는 모든 frame_id 기준
    frame_ids = sorted(set(map(int, user_pose_dict.keys())) | set(map(int, ref_pose_dict.keys())))

    for frame_id in frame_ids:
        vis = np.ones((h, w, 3), dtype=np.uint8) * 255  # 흰 배경

        user_pose = normalize_keys(user_pose_dict.get(str(frame_id), {}))
        ref_pose = normalize_keys(ref_pose_dict.get(str(frame_id), {}))

        draw_pose(vis, user_pose, (255, 0, 0), w, h)
        draw_pose(vis, ref_pose, (0, 255, 0), w, h)

        cv2.putText(vis, f"Frame: {frame_id}", (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

        cv2.imshow('Pose Only', cv2.resize(vis, None, fx=0.5, fy=0.5))
        if cv2.waitKey(500) & 0xFF == 27:
            break

        out.write(vis)

    out.release()
    cv2.destroyAllWindows()
    print(f"[✅] 저장 완료: {output_path}")




# ────────────────────────────────
with open("D:\\LearningPython\\capston\\originalKeypoints\\test_user_pose_normalized.json") as f:
    user_pose_dict = json.load(f)

with open("D:\\LearningPython\\capston\\originalKeypoints\\test_ref_pose_normalized.json") as f:
    ref_pose_dict = json.load(f)

draw_skeletons_without_video(
    user_pose_dict=user_pose_dict,
    ref_pose_dict=ref_pose_dict,
    output_path="D:\\LearningPython\\capston\\outputVideos\\pose_only_overlay.mp4"
)
