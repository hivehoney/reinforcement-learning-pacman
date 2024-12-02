from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense
import numpy as np

class NeuralNetwork:
    def __init__(self, input_size, output_size):
        self.input_size = input_size
        self.output_size = output_size
        self.model = Sequential([
            Dense(10, input_shape=(4,), activation='relu'),  # 입력층 → 은닉층 1
            Dense(20, activation='relu'),                   # 은닉층 1 → 은닉층 2
            Dense(10, activation='relu'),                   # 은닉층 2 → 은닉층 3
            Dense(output_size, activation='softmax')        # 은닉층 3 → 출력층
        ])

    def total_weights(self):
        """모든 가중치와 편향 개수를 반환"""
        weights = self.model.get_weights()
        return sum(w.size for w in weights)

    def set_weights(self, genes):
        """유전자를 신경망 가중치로 설정"""
        weights = self.model.get_weights()
        index = 0
        new_weights = []
        for w in weights:
            shape = w.shape
            size = np.prod(shape)
            new_weights.append(np.array(genes[index:index+size]).reshape(shape))
            index += size
        self.model.set_weights(new_weights)

    def predict(self, inputs):
        """입력값에 대한 출력값 계산"""
        return self.model.predict(np.array([inputs]))[0]
