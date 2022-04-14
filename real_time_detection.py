import numpy as np
import telegram
import time
from serial_plot import serialPlot
from test import Gesture_Detection
from pynq import Overlay
from telegram_bot import telegram_bot


class Detection():
    def __init__(self, model, SerialData, windows_size=100, threshold=0.35, hit_threshold=5) -> None:
        self.model = model
        bot.send_message(chat_id=id, text="Start loading model...")
        print("Start loading model...")
        self.Gesture_model = Gesture_Detection(model, windows_size=windows_size)
        print("Finish loading model!")
        bot.send_message(chat_id=id, text="Finish loading model!")
        leds[0:4].write(15)
        self.SerialData = SerialData
        self.windows_size = windows_size
        self.threshold = threshold
        self.hit_threshold = hit_threshold
        self.continue_count = 0
        self.pre_result = None
        bot.send_message(chat_id=id, text="Start detecting and classifying ...")
    def get_serial_data(self):
        data = self.SerialData.getSerialData()
        return data

    def gen_predict_data(self, data) -> dict:
        g_p = np.array(data).T
        result_predict = self.Gesture_model.predict_2(g_p)
        return result_predict

    def post_process(self, data) -> bool:
        # print(data['hm_max_value'],self.continue_count)
        if data['hm_max_value'] > self.threshold:
            if self.pre_result is not None:
                if self.pre_result == data['class']:
                    self.continue_count += 1
                else:
                    self.pre_result = data['class']
            else:
                self.pre_result = data['class']
        else:
            self.pre_result == None
            self.continue_count = 0
            return False
        print(data['hm_max_value'], self.continue_count)

        if self.continue_count == self.hit_threshold:
            return True
        else:
            return False

    def start_detection(self):
        global start
        while True:
            start = time.time()
            data = self.get_serial_data()
            result_predict = self.gen_predict_data(data)
            res = 0
            if self.post_process(result_predict):
                res = result_predict['class'] + 1

            yield res

def main():
    model_name = "Unet_classify_win_100_wh_0.1_focal_ahpha2_beta4_2021-08-16-15-13-56"
    windows_size = 100
    portName = '/dev/ttyACM0'  # for windows users
    baudRate = 115200
    maxPlotLength = windows_size
    dataNumBytes = 4  # number of bytes of 1 data point
    dataInNum = 3
    s = serialPlot(portName, baudRate, maxPlotLength, dataNumBytes, dataInNum)  # initializes all required variables
    s.readSerialStart()
    try:
        dect = Detection(model=model_name, SerialData=s, hit_threshold=2)
        time.sleep(2)
        for res in dect.start_detection():
            if res != 0:
                end = time.time()
                print(f"Model calculation cost:{end-start} s")
                img_dict = {1: 'https://i.imgur.com/8q9jUXE.png', 2: 'https://i.imgur.com/OZi1Qj3.png',
                            3: 'https://i.imgur.com/l7u8PWe.png', 4: 'https://i.imgur.com/HiF1rIy.png',
                            5: 'https://i.imgur.com/z1cZbjp.png'}
                photo = bot.send_photo(chat_id=id, photo=img_dict[res])
                leds[0:4].write(res)
                message = bot.send_message(chat_id=id, text=f"Detect result: {res}")
                time.sleep(2)
                bot.delete_message(chat_id=id, message_id=photo.message_id)
                bot.delete_message(chat_id=id, message_id=message.message_id)
                print(f"Detect result: {res}")
            else:#res==0
                leds[0:4].write(0)
    finally:
        s.close()


if __name__ == "__main__":
    id = "1928130820"
    token = "1997238109:AAFrdEtGSNVzYvX_9JDvuK9C_5o6My7qjto"
    bot = telegram.Bot(token=token)
    bot.send_message(chat_id=id, text="Running real_time_detection.py")
    base = Overlay('./overlay/test.bit')  # IP setting from vivado
    leds = base.axi_gpio_0  # the name of the IP object ([0:4]:only 4 leds)
    main()
