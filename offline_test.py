import os,glob,time
import numpy as np
import threading
from keras.models import load_model
import tensorflow as tf
from GN import GroupNormalization
from model_Oap_gntfatypes import OaP_GD_loss

def job(queue,window_size,count):
    global PKI_t, SKI_t ,PKI_c ,SKI_c
    Threshold = 0.6
    gesN=3
    dim =6
    Tmin = 0
    Tmax = 100
    window = queue[:]                    # window是queue的複製品(50,6)
    window = np.array([window])          # (1,50,6)
    window.reshape(1, window_size, dim)    # 將50個Sample點製作成window shape
    window = window.astype("float32")
    pre_start = time.time()
    pre = func(window)
    pre_end = time.time()
    #pre = model_OaP.predict(window)      # 將window輸入至模型進行predict
    for i in range(2):
        queue.pop(0)                     # sliding window , stride_size=2
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
                print(f"Gesture dected : {result}")
                print(f"window cost:{pre_end-pre_start} s")
                print(f"total cost:{endtime-starttime} s")
                print()
                PKI_t, PKI_c, SKI_t, SKI_c = 0, 0, 0, 0
                return result
def read_samples(test_path):
    global count ,starttime,is_detected
    queue = []
    window_size = 50
    for label in os.listdir(test_path):
        for txtfile in glob.glob(test_path+"/"+label+"/*.txt"):
            with open(txtfile) as test_case:
                starttime = time.time()
                for line in test_case:
                    try:
                        s = line[:-2].split(' ')
                        count += 1
                        queue.append(list(map(float,s)))
                    except ValueError:
                        print("ValueError")
                    if len(queue) == window_size:
                        res = job(queue, window_size, count)
                        if res:
                            count = 0
                            break

if __name__ == '__main__':
    model_OaP = load_model("./model/best_OaP_SAM_anchor2_32_0911_.h5",custom_objects={
        'OaP_GD_loss':OaP_GD_loss,
        'GroupNormalization':GroupNormalization})
    test_base_dir = "./test_data"
    batch_size =1
    input_shape = model_OaP.inputs[0].shape.as_list()
    input_shape[0] = batch_size
    func = tf.function(model_OaP).get_concrete_function(
        tf.TensorSpec(input_shape, model_OaP.inputs[0].dtype))
    count= 0
    PKI_t,PKI_c,SKI_t,SKI_c=0,0,0,0
    read_samples(test_base_dir)
