# pynqz2_hackathon_phone_ges

PYNQ-z2 Environment Setup : 

tensorflow 2.3.0 & python3.7 on PYNQ-z2 

Install setps followed by https://github.com/rockman4308/MC2_gesture_detection_pynqz2_tensorflow 

    * pip install paho-mqtt
    * pip install python-telegram-bot-raw --upgrade
   

Android APP setup : 
Just put apk into your android phone .

    * MQTT_in0.apk

We use supervisor to automatically execute our mqtt_receiver.py or you could directly use python interpreter to do it.

    * sudo apt-get install supervisor 
    * sudo nano /etc/supervisor/conf.d/mqtt.conf
    * sudo chmod 775 mqtt.conf
    * sudo supervisorctl update
    * sudo supervisorctl start mqtt
    
    # python3 mqtt_receiver.py

