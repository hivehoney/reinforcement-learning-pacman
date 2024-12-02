import numpy as np
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense


class NeuralNetwork:
    """
    신경망 클래스
    - 유전 알고리즘과 연동하여 팩맨의 행동을 학습시키는 역할을 담당
    """
    def __init__(self, input_size, output_size):
        """
        NeuralNetwork 클래스의 초기화 메서드
        - 입력층, 은닉층, 출력층으로 구성된 신경망 생성

        Args:
            input_size (int): 입력층의 뉴런 개수
            output_size (int): 출력층의 뉴런 개수
        """
        self.input_size = input_size  # 입력값의 크기
        self.output_size = output_size  # 출력값의 크기 (UP, DOWN, LEFT, RIGHT / [0,0,0,0])
        # 신경망 모델 정의
        self.model = Sequential([
            Dense(10, input_shape=(4,), activation='relu'),  # 입력층 → 은닉층 1
            Dense(20, activation='relu'),                   # 은닉층 1 → 은닉층 2
            Dense(10, activation='relu'),                   # 은닉층 2 → 은닉층 3
            Dense(output_size, activation='softmax')        # 은닉층 3 → 출력층
        ])

    def total_weights(self):
        """
        신경망의 전체 가중치 및 편향 개수를 반환
        - 유전 알고리즘에서 유전자 길이를 설정하기 위해 사용

        Returns:
            int: 신경망 가중치 및 편향의 총 개수
        """
        weights = self.model.get_weights()  # 각 층의 가중치와 편향 리스트
        return sum(w.size for w in weights)  # 모든 가중치와 편향 요소 개수를 합산

    def set_weights(self, genes):
        """
        유전 알고리즘에서 생성된 유전자를 신경망의 가중치로 설정
        - 유전자는 4배열 형태로 전달

        genes (list): 신경망 가중치 및 편향에 해당하는 유전자 리스트
        """
        weights = self.model.get_weights()  # 기존 신경망 가중치와 편향 리스트
        index = 0  # 유전자 리스트에서의 시작 인덱스
        new_weights = []

        # 각 층의 가중치/편향을 유전자로 대체
        for w in weights:
            shape = w.shape  # 현재 가중치/편향의 shape
            size = np.prod(shape)  # 요소 개수 계산
            new_weights.append(np.array(genes[index:index + size]).reshape(shape))
            index += size

        self.model.set_weights(new_weights)  # 변환된 가중치와 편향 설정

    def predict(self, inputs):
        """
        입력값에 대해 신경망의 출력값을 계산
        - 팩맨의 위치와 가장 가까운 유령의 상대적 위치를 입력으로 받아 방향을 출력
        inputs (list): 입력값 리스트 ([팩맨 x좌표, 팩맨 y좌표, 유령 x좌표, 유령 y좌표])

        Returns:
            list: 신경망 출력값
        """
        return self.model.predict(np.array([inputs]))[0]
