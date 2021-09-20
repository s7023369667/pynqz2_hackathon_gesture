import paho.mqtt.client as mqtt
import time,threading
import numpy as np
from keras.models import load_model
from GN import GroupNormalization
from model_Oap_gntfatypes import OaP_GD_loss
import tensorflow as tf
from telegram_bot import telegrambot
##receiver
def on_connect(client, userdata, flags, rc):
    tb.send_message("Connected with mosquitto broker.")
    client.subscribe("mqtt")   #topic : mqtt

def on_message(client, userdata, msg):
    global queue,count,starttime,is_detected
    window_size = 50
    count += 1
    if len(queue)==0:
        is_detected=False
    if not is_detected:
        try:
            message = (msg.payload.decode()).split(' ')
            if len(message) != 6:
                raise ValueError
            queue.append(list(map(float, message)))  # (1,50,6)
        except ValueError:
            pass
        if len(queue) == window_size:
            job(window_size,count)

def job(window_size,count):
    global PKI_t, SKI_t ,PKI_c ,SKI_c,queue,starttime,is_detected 
    is_detected = False
    Threshold = 0.7
    Tmin = 0
    Tmax = 100
    window = queue[:]                    # window是queue的複製品(50,6)
    window = np.array([window])          # (1,50,6)
    window.reshape(1, window_size, 6)    # 將50個Sample點製作成window shape
    window = window.astype("float32")
    pre_start = time.time()
    pre = func(window)
    pre_end = time.time()
    #pre = model_OaP.predict(window)      # 將window輸入至模型進行predict
    for i in range(2):
        queue.pop(0)                      # sliding window , stride_size=2
    """match algorithm"""
    PKI_arg = np.argmax(pre[1])
    SKI_arg = np.argmax(pre[2])
    match_time = count - window_size
    if PKI_arg != 0:
        if pre[1][0][PKI_arg] >= Threshold:
            PKI_t = match_time
            PKI_c = PKI_arg
    if SKI_arg != 0:
        if pre[2][0][SKI_arg] >= Threshold:
            SKI_t = match_time
            SKI_c = SKI_arg
            if (PKI_c == SKI_c) & (SKI_t - PKI_t >= Tmin) & (SKI_t - PKI_t <= Tmax):
                endtime = time.time()
                result = SKI_c+(11-gesN)
                print(f"Gesture {result}")
                print(f"Winow cost : {pre_end-pre_start}")
                print(f"Total cost : {endtime-starttime}")
                starttime = time.time()
                tb.send_photo(result)
                is_detected = True
                queue = []
                PKI_t, PKI_c, SKI_t, SKI_c = 0, 0, 0, 0
                starttime = time.time()


if __name__ == '__main__':
    ##initialization
    tb = telegrambot()
    model_name = 'best_OaP_SAM_anchor2_32_0911_.h5'
    tb.send_message("Start loading model ...")
    model_OaP = load_model(f"./model/{model_name}", custom_objects={
        'OaP_GD_loss': OaP_GD_loss,'GroupNormalization':GroupNormalization })
    batch_size =1
    input_shape = model_OaP.inputs[0].shape.as_list()
    input_shape[0] = batch_size
    func = tf.function(model_OaP).get_concrete_function(
        tf.TensorSpec(input_shape, model_OaP.inputs[0].dtype))
    tb.send_message("Finish loading model...")
    queue = []
    count,is_detected = 0,False 
    gesN=2
    PKI_t,PKI_c,SKI_t,SKI_c=0,0,0,0
    ##connecting with mqtt broker
    starttime = time.time()
    client = mqtt.Client()  # client_id
    client.on_connect = on_connect
    client.on_message = on_message
    #client.username_pw_set("xilinx","xilinx")
    client.connect("localhost", 1883)
    client.loop_forever()
