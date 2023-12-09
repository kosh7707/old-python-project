import tensorflow as tf
from tensorflow.keras import *
import numpy as np
import cv2
import logging

tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
# --------------------------------------------------------------------------------------------------------------
characters = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
char_to_num = layers.experimental.preprocessing.StringLookup(
    vocabulary=characters, num_oov_indices=0, mask_token=None
)
num_to_char = layers.experimental.preprocessing.StringLookup(
    vocabulary=char_to_num.get_vocabulary(), num_oov_indices=0, mask_token=None, invert=True
)
image_width = 110
image_height = 40
# --------------------------------------------------------------------------------------------------------------
class CTCLayer(layers.Layer):
    def __init__(self, name=None, **kwargs):
        super().__init__(name=name)
        self.loss_fn = backend.ctc_batch_cost

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
# --------------------------------------------------------------------------------------------------------------
def encode_single_sample(image_path, label):
    image = tf.io.read_file(image_path)
    image = tf.io.decode_png(image, channels=1)
    image = tf.image.convert_image_dtype(image, tf.float32)
    image = tf.image.resize(image, [image_height, image_width])
    image = tf.transpose(image, perm=[1, 0, 2])
    label = char_to_num(tf.strings.unicode_split(label, input_encoding='UTF-8'))
    return {'image': image, 'label': label}
# --------------------------------------------------------------------------------------------------------------
def decode_batch_predictions(pred):
    max_length = 4
    input_len = np.ones(pred.shape[0]) * pred.shape[1]
    results = backend.ctc_decode(pred, input_length=input_len, greedy=True)[0][0][:, :max_length]
    output_text = []
    for res in results:
        res = tf.strings.reduce_join(num_to_char(res)).numpy().decode('utf-8')
        output_text.append(res)
    return output_text
# --------------------------------------------------------------------------------------------------------------
def model_load():
    model = models.load_model('./model.h5', custom_objects={'CTCLayer': CTCLayer})    # 모델 불러오기
    prediction_model = models.Model(
        model.get_layer(name='image').input, model.get_layer(name='dense2').output
    )
    return prediction_model
# --------------------------------------------------------------------------------------------------------------
def OCRModelLoad(prediction_model):
    test = OCR('./image/test.png', prediction_model)
# --------------------------------------------------------------------------------------------------------------
def OCR(image_path, prediction_model):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    ret, thr = cv2.threshold(image, 60, 255, cv2.THRESH_BINARY)
    image_path_thr = image_path[:-4] + '_thr.png'
    cv2.imwrite(image_path_thr, thr)
    image_path = [image_path_thr]
    label = ['0043']
    ds = tf.data.Dataset.from_tensor_slices((image_path, label))
    ds = ds.map(encode_single_sample).batch(1)
    data = tf.data.Dataset.get_single_element(ds)
    preds = prediction_model.predict(data)
    ret = decode_batch_predictions(preds)
    return ret[0]
# --------------------------------------------------------------------------------------------------------------

