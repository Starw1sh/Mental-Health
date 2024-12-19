import cv2
import dlib
import numpy as np
from PIL import Image
import pandas as pd
import os
import subprocess
import shutil
# 路径设置
input_video_path = r"D:\Study_Files\2.0\XingCe\myTest\upload\video"  # 输入视频目录
frame_output_path = r"D:\Study_Files\2.0\XingCe\myTest\backend\extracted_frames"  # 视频帧存储目录
face_output_path = r"D:\Study_Files\2.0\XingCe\myTest\backend\output_faces"  # 人脸裁剪存储目录
openface_feature_path = r"D:\Study_Files\2.0\XingCe\myTest\backend\openface_features"  # OpenFace 提取特征存储目录
openface_binary_path = "/path/to/OpenFace/build/bin/FeatureExtraction"  # OpenFace FeatureExtraction 路径

# 确保输出目录存在
os.makedirs(frame_output_path, exist_ok=True)
os.makedirs(face_output_path, exist_ok=True)
os.makedirs(openface_feature_path, exist_ok=True)

# print("makesure")
shutil.rmtree(frame_output_path)
os.makedirs(frame_output_path)
shutil.rmtree(face_output_path)
os.makedirs(face_output_path)
shutil.rmtree(openface_feature_path)
os.makedirs(openface_feature_path)
# print("finish empty")
# 加载人脸检测模型 (使用 dlib)
detector = dlib.get_frontal_face_detector()


def extract_frames_from_video(video_path, output_path, fps=1):
    """从视频中提取帧，每秒保存一帧"""
    cap = cv2.VideoCapture(video_path)
    video_fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = int(video_fps // fps)  # 计算帧间隔
    frame_count = 0
    extracted_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if frame_count % frame_interval == 0:  # 按间隔提取帧
            frame_filename = os.path.join(output_path,
                                          f"{os.path.basename(video_path).split('.')[0]}_frame_{extracted_count}.jpg")
            cv2.imwrite(frame_filename, frame)
            extracted_count += 1
        frame_count += 1

    cap.release()
    # print(f"从视频 {video_path} 提取了 {extracted_count} 帧")


def extract_and_save_faces(image_path, output_path, scale=1.2):
    """提取人脸并保存放大后的区域"""
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    for i, face in enumerate(faces):
        x1, y1, x2, y2 = face.left(), face.top(), face.right(), face.bottom()
        # 放大坐标
        width, height = x2 - x1, y2 - y1
        x1 = max(0, int(x1 - width * (scale - 1) / 2))
        y1 = max(0, int(y1 - height * (scale - 1) / 2))
        x2 = min(image.shape[1], int(x2 + width * (scale - 1) / 2))
        y2 = min(image.shape[0], int(y2 + height * (scale - 1) / 2))

        # 截取并保存
        face_image = image[y1:y2, x1:x2]
        output_file = os.path.join(output_path, f"{os.path.basename(image_path).split('.')[0]}_face_{i}.jpg")
        cv2.imwrite(output_file, face_image)


def process_images_with_openface(input_path, output_path):
    """利用 OpenFace 提取面部特征"""
    # 调用 OpenFace 的 FeatureExtraction 命令
    command = [
        openface_binary_path,
        "-fdir", input_path,
        "-out_dir", output_path
    ]
    subprocess.run(command)


def collect_features_from_csv(csv_dir):
    """收集 OpenFace 生成的特征 CSV 文件并汇总"""
    features = []
    for file in os.listdir(csv_dir):
        if file.endswith(".csv"):
            file_path = os.path.join(csv_dir, file)
            df = pd.read_csv(file_path)
            features.append(df)
    return pd.concat(features, ignore_index=True)


# 主流程
def main():
    # 1. 从视频中提取帧
    for file in os.listdir(input_video_path):
        if file.lower().endswith(('.mp4', '.avi', '.mkv', '.mov')):
            extract_frames_from_video(
                os.path.join(input_video_path, file),
                frame_output_path
            )

    # 2. 提取并保存帧中的人脸
    for file in os.listdir(frame_output_path):
        if file.lower().endswith(('.png', '.jpg', '.jpeg')):
            extract_and_save_faces(
                os.path.join(frame_output_path, file),
                face_output_path
            )

    # 从此往下的可以复用图像处理算法
    # 3. 使用 OpenFace 提取特征
    # process_images_with_openface(face_output_path, openface_feature_path)

    # # 4. 汇总特征到一个 CSV 文件
    # features_df = collect_features_from_csv(openface_feature_path)
    # features_df.to_csv("video_extracted_features.csv", index=False)
    # print("特征提取完成，已保存至 video_extracted_features.csv")

if __name__ == "__main__":
    main()