# ImgDataGenerator Class

import pandas as pd
import numpy as np
import json
import tensorflow as tf
from tensorflow.keras.utils import to_categorical
import cv2               # OpenCV 라이브러리 가져오기

# 파일을 하나씩 넘겨주는 generator
class ImgDataGenerator(tf.keras.utils.Sequence):
    def __init__(self, df_files, input_shape, batchsize, label_names, num_files, lw=3, state='Train', smoothing_factor=0.1):
        # 클래스 초기화 함수
        self.df_files = sorted(df_files)[:num_files]  # 데이터프레임 파일 리스트, 파일명 기준 오름차순 정렬 후 지정된 개수만큼 선택
        self.file_sel = 0  # 현재 사용할 파일 인덱스
        self.batchsize = batchsize  # 배치 크기
        self.input_shape = input_shape  # 입력 이미지 모양
        self.label_names = label_names  # 레이블 이름
        self.lw = lw  # 선의 너비
        self.state = state  # 상태 (Train, Test)
        self.smoothing_factor = smoothing_factor  # 스무딩 팩터
        self.on_epoch_end()  # epoch 종료시 호출

    def smooth_labels(self, labels):
        # 레이블을 부드럽게 만드는 함수
        labels *= (1 - self.smoothing_factor)
        labels += (self.smoothing_factor / len(self.label_names))
        return labels

    def __len__(self):
        # 데이터셋의 길이 반환
        return -(-len(self.df) // self.batchsize)

    def draw_strokes(self, raw_strokes, image_size=128, line_width=6):
        self.border_offset = line_width * 2  # 테두리 공백 크기
        self.stroke_list = []  # raw_strokes를 NumPy 배열로 변환한 리스트
        self.bounds_info = {"min_x": float('inf'), "min_y": float('inf'),    # 최소 x, y 좌표 초기화
                            "max_x": float('-inf'), "max_y": float('-inf')}  # 최대 x, y 좌표 초기화

        # raw_strokes의 각 stroke에 대해 NumPy 배열로 변환하고 경계 좌표 갱신
        for stroke in raw_strokes:
            self.np_stroke = np.array(stroke)  # stroke를 NumPy 배열로 변환
            self.stroke_list.append(self.np_stroke)    # 변환된 배열을 stroke_list에 추가
            self.bounds_info["min_x"] = min(self.bounds_info["min_x"], min(self.np_stroke[0]))
            self.bounds_info["max_x"] = max(self.bounds_info["max_x"], max(self.np_stroke[0]))
            self.bounds_info["min_y"] = min(self.bounds_info["min_y"], min(self.np_stroke[1]))
            self.bounds_info["max_y"] = max(self.bounds_info["max_y"], max(self.np_stroke[1]))

        # 빈 이미지 생성
        self.new_image = np.zeros((image_size, image_size, 3), dtype=float)
        self.original_width = self.bounds_info["max_x"] - self.bounds_info["min_x"]  # 원본 그림의 너비
        self.original_height = self.bounds_info["max_y"] - self.bounds_info["min_y"]  # 원본 그림의 높이
        self.ratio = max(self.original_width, self.original_height) / (image_size - self.border_offset * 2)  # 비율 계산

        # 비율이 0일 경우 빈 이미지 반환
        if self.ratio == 0:
            return self.new_image

        # 각 stroke의 좌표를 새로운 크기에 맞게 조정하여 이미지에 그리기
        for self.np_stroke in self.stroke_list:
            self.np_stroke[0] = (self.np_stroke[0] - self.bounds_info["min_x"]) / self.ratio + self.border_offset  # x 좌표 조정
            self.np_stroke[1] = (self.np_stroke[1] - self.bounds_info["min_y"]) / self.ratio + self.border_offset  # y 좌표 조정
            
            # 선 그리기
            for i in range(len(self.np_stroke[0]) - 1):
                self.start_x, self.start_y = int(self.np_stroke[0][i]), int(self.np_stroke[1][i])  # 시작점 좌표
                self.end_x, self.end_y = int(self.np_stroke[0][i + 1]), int(self.np_stroke[1][i + 1])  # 끝점 좌표
                self.new_image = cv2.line(self.new_image, 
                                          (self.start_x, self.start_y), 
                                          (self.end_x, self.end_y), 
                                          (255, 255, 255), line_width)  # 선 그리기

        return self.new_image  # 완성된 이미지 반환
    
    def __getitem__(self, index):
        # 주어진 인덱스에 해당하는 데이터 가져오기
        try:
            batch_idx = self.idx[index * self.batchsize:(index + 1) * self.batchsize]
            h, w, ch = self.input_shape
            X = np.zeros((len(batch_idx), h, w, ch))
            y = np.zeros((len(batch_idx), len(self.label_names)))

            for i, idx in enumerate(batch_idx):
                row = self.df.iloc[idx]
                raw_strokes = json.loads(row['drawing'])
                # draw_strokes 함수 호출하여 이미지 데이터 생성
                X[i, :, :, ] = self.draw_strokes(raw_strokes, image_size=h, line_width=self.lw)

                if self.state != 'Test':
                    label_index = row['y']
                    label = to_categorical(label_index, num_classes=len(self.label_names))
                    y[i, :] = self.smooth_labels(label)

            return (X, y) if self.state != 'Test' else X
        except Exception as e:
            print(f"오류가 발생한 파일: {self.df_files[self.file_sel]}")
            print(f"오류 상세 정보: {e}")
            raise e

    def on_epoch_end(self):
        # epoch 종료시 호출되는 함수
        try:
            self.df = pd.read_csv(self.df_files[self.file_sel], compression='gzip')  # .gz 파일 읽기 추가
            self.idx = np.tile(np.arange(len(self.df)), 2)
            if self.state == 'Train':
                np.random.shuffle(self.idx)
            self.file_sel = (self.file_sel + 1) % len(self.df_files)
        except Exception as e:
            print(f"파일 읽기 중 오류 발생: {self.df_files[self.file_sel]}")
            print(f"오류 상세 정보: {e}")
            raise e