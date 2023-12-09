# tensorflow, scikit-learn 설치
import sys
import os
import tensorflow as tf
from glob import glob
from tensorflow import keras
from tensorflow.keras import layers
from sklearn.model_selection import train_test_split

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'        # warning 제거

image_list = glob('./thr_images/*.png')

images = []     # image_paths
labels = []     # 각 image_path의 label
max_length = 4

for image_path in image_list:
    images.append(image_path)

    label = os.path.splitext(os.path.basename(image_path))[0][0:4] # 각 image의 파일명이 곧 라벨이기 떄문에 사용
    labels.append(label)

# ------------------------------------------------------------------------------------------------------------------------------------------------------
'''
아래는 전처리 과정이다. StringLookup은 문자열 범주형 값을 정수 인덱스로 바꾸는 것이다.
즉, 하나의 문자에 하나의 정수값이 대응되게 만드는 것이다.
필요한 과정이라하니 일단 외우자.
labels[1] --> '0044'
encoded = char_to_num(tf.strings.unicode_split(labels[1], input_encoding='UTF-8'))
    --> <tf.Tensor: shape=(4,), dtype=int64, numpy=array([0, 0, 4, 4], dtype=int64)>
후에 결과를 다시 불러올때 num_to_char로 이어붙이면 아래와 같이 된다.
tf.strings.reduce_join(num_to_char(encoded)).numpy().decode('utf-8')
    --> '0044'
이는 내가 characters를 0~9만 해서 그렇지 각종 문자와 알파벳이 섞이게 된다고 생각하면 감이 온다.
'''
characters = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

char_to_num = layers.experimental.preprocessing.StringLookup(
    vocabulary=characters, num_oov_indices=0, mask_token=None
)

num_to_char = layers.experimental.preprocessing.StringLookup(
    vocabulary=char_to_num.get_vocabulary(), num_oov_indices=0, mask_token=None, invert=True
)

# ------------------------------------------------------------------------------------------------------------------------------------------------------
'''
transpose를 하는 이유 설명
앞으로 이미지를 모델에 넣을건데 모델이 이미지의 앞부분부터 읽어들이길 원함.
하지만 모델은 위에서부터 아래로 읽기 때문에 한글자씩 읽게 하려면 이미지를 세워야함.
--> transpose 사용
'''
image_width = 110
image_height = 40
def encode_single_sample(image_path, label):
    image = tf.io.read_file(image_path)                             # 이미지 파일 읽기
    image = tf.io.decode_png(image, channels=1)                     # png로 인코딩된 이미지를 uint8로 디코딩, channels --> 색상 채널 수 (0은 원래 파일의 채널)
    image = tf.image.convert_image_dtype(image, tf.float32)         # 이미지의 date type 변경
    image = tf.image.resize(image, [image_height, image_width])     # 이미지 리사이징, 혹시라도 다를 수 있는 이미지들의 크기 균일화
    image = tf.transpose(image, perm=[1, 0, 2])                     # 이미지 전치 (transpose==전치행렬), 이미지를 세로로 세운다고 생각하면 됨.
    label = char_to_num(tf.strings.unicode_split(label, input_encoding='UTF-8'))
    return {'image': image, 'label': label}

# ------------------------------------------------------------------------------------------------------------------------------------------------------
'''
참고 : https://teddylee777.github.io/scikit-learn/train-test-split
train용 데이터와 validation용 데이터를 나누는 과정이다.
'''
x_train, x_val, y_train, y_val = train_test_split(images, labels, test_size=0.15, random_state=2021)

# ------------------------------------------------------------------------------------------------------------------------------------------------------
'''
이제 dataset을 정의해주자.
train_dataset과 validation_dataset(유효성검증용 테스트셋)을 나눠주는 과정이다.
batch가 뭔지, 이외에도 부족한 지식에 괜찮은 설명이 들어간 아래 사이트를 읽어보자.
참고 : https://gooopy.tistory.com/68
tf.data.Dataset을 쓰는이유 --> 최적화가 아주 잘되어있어서 빠르고 편함.
tf.data.experimental.AUTOTUNE --> tf.data 런타임에 가용되는 병렬화 수준을 결졍함.
참고 : https://ahnjg.tistory.com/32
'''
batch_size = 32

train_dataset = tf.data.Dataset.from_tensor_slices((x_train, y_train))
train_dataset = (
    train_dataset.map(
        encode_single_sample, num_parallel_calls=tf.data.experimental.AUTOTUNE
    )
    .batch(batch_size)
    .prefetch(buffer_size=tf.data.experimental.AUTOTUNE)
)

validation_dataset = tf.data.Dataset.from_tensor_slices((x_val, y_val))
validation_dataset = (
    validation_dataset.map(
        encode_single_sample, num_parallel_calls=tf.data.experimental.AUTOTUNE
    )
    .batch(batch_size)
    .prefetch(buffer_size=tf.data.experimental.AUTOTUNE)
)

# ------------------------------------------------------------------------------------------------------------------------------------------------------
'''
대망의 모델 정의 부분이다.
CTCLayer라고 하는 모델인데 아래 링크를 참고하자.
참고 : https://ratsgo.github.io/speechbook/docs/neuralam/ctc
아래 모델을 이해하는것도 좋지만 아직 배울게 많으니.. 그냥 갖다 쓰자.
'''
class CTCLayer(layers.Layer):
    def __init__(self, name=None, **kwargs):
        super().__init__(name=name)
        self.loss_fn = keras.backend.ctc_batch_cost

    def call(self, y_true, y_pred):
        # Compute the training-time loss value and add it
        # to the layer using `self.add_loss()`.
        batch_len = tf.cast(tf.shape(y_true)[0], dtype='int64')
        input_length = tf.cast(tf.shape(y_pred)[1], dtype='int64')
        label_length = tf.cast(tf.shape(y_true)[1], dtype='int64')

        input_length = input_length * tf.ones(shape=(batch_len, 1), dtype='int64')
        label_length = label_length * tf.ones(shape=(batch_len, 1), dtype='int64')

        loss = self.loss_fn(y_true, y_pred, input_length, label_length)
        self.add_loss(loss)

        # At test time, just return the computed predictions
        return y_pred

# ------------------------------------------------------------------------------------------------------------------------------------------------------
'''
위 CTCLayer를 이용해서 모델을 만들자.
모르는 부분이 상당히 많다. 왜 하는지도 모르겠다. 일단 아래 링크를 참고하자.
참고 : https://guru.tistory.com/70
Conv2D -> MaxPooling2D -> Conv2D -> MaxPooling2D
'합성곱 신경망(CNN)' 이라는 것이라 한다. (이미지 처리에 탁월한 신경망이라는데..)
참고 : https://wikidocs.net/64066 <-- 생각보다 이해가 잘된다. 정신을 맑게 하고 정독해보자.
밑에 '순환 신경망(RNN)'도 있는데 이 또한 아래 링크를 참고하자.
참고 : https://wikidocs.net/22886
마치 모델이라는 정수기 필터를 데이터라는 물이 따라가는 느낌이다.
입력이 layer(name = 'image'), 
출력이 layer(name = 'dense2') 라는 것만 알고 넘어가자.

model = keras.models.Model(
    inputs=[input_img, labels], outputs=output, name='ocr_model_v1'
)
이 부분을 유심히 볼 필요가 있다.
'''
def build_model():
    # Inputs to the model
    input_img = layers.Input(
        shape=(image_width, image_height, 1), name='image', dtype='float32'
    )
    labels = layers.Input(name='label', shape=(None,), dtype='float32')

    # First conv block
    x = layers.Conv2D(
        32,
        (3, 3),
        activation='relu',
        kernel_initializer='he_normal',
        padding='same',
        name='Conv1',
    )(input_img)
    x = layers.MaxPooling2D((2, 2), name='pool1')(x)

    # Second conv block
    x = layers.Conv2D(
        64,
        (3, 3),
        activation='relu',
        kernel_initializer='he_normal',
        padding='same',
        name='Conv2',
    )(x)
    x = layers.MaxPooling2D((2, 2), name='pool2')(x)

    # We have used two max pool with pool size and strides 2.
    # Hence, downsampled feature maps are 4x smaller. The number of
    # filters in the last layer is 64. Reshape accordingly before
    # passing the output to the RNN part of the model
    new_shape = ((image_width // 4), (image_height // 4) * 64)
    x = layers.Reshape(target_shape=new_shape, name='reshape')(x)
    x = layers.Dense(64, activation='relu', name='dense1')(x)
    x = layers.Dropout(0.2)(x)

    # RNNs
    x = layers.Bidirectional(layers.LSTM(128, return_sequences=True, dropout=0.25))(x)
    x = layers.Bidirectional(layers.LSTM(64, return_sequences=True, dropout=0.25))(x)

    # Output layer
    x = layers.Dense(
        len(char_to_num.get_vocabulary()) + 1, activation='softmax', name='dense2'
    )(x)

    # Add CTC layer for calculating CTC loss at each step
    output = CTCLayer(name='ctc_loss')(labels, x)

    # Define the model
    model = keras.models.Model(
        inputs=[input_img, labels], outputs=output, name='ocr_model_v1'
    )
    # Optimizer
    opt = keras.optimizers.Adam()
    # Compile the model and return
    model.compile(optimizer=opt)
    return model

# Get the model
model = build_model()

# ------------------------------------------------------------------------------------------------------------------------------------------------------
'''
실질적으로 학습을 시작하는 부분이다.
EarlyStopping은 학습이 진전이 없을 경우(10번이상 val_loss가 변화가 없을 경우) 
더 이상 학습을 하지 않고 val_loss가 가장 적었던 부분의 wieghts를 얻게 된다.
이상하게 멈춰서 patience 부분을 50으로 고쳐주고 학습을 시작했다.
'''
early_stopping = keras.callbacks.EarlyStopping(
    monitor='val_loss', patience=50, restore_best_weights=True
)

history = model.fit(
    train_dataset,
    validation_data=validation_dataset,
    epochs=200,
    callbacks=[early_stopping],
)

# ------------------------------------------------------------------------------------------------------------------------------------------------------
'''
얻은 모델을 저장하자.
'''
model.save('./model.h5')
sys.exit()


