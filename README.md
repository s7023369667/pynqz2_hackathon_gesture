# pynqz2_hackathon_phone_ges

PYNQ-Z2 Environment Setup : 

tensorflow 2.3.0 & python3.7 on PYNQ-z2 

Install steps followed by https://github.com/rockman4308/MC2_gesture_detection_pynqz2_tensorflow 

Install mosquitto broker and start the service on PYNQ-Z2: 
    
    * sudo apt-get install mosquitto
    * sudo service mosquitto start 
    
    ##Check if the MQTT broker is running or not ?
    ##You will see the default port:1883 is "LISTEN"
    * netstat –at    

Install other python packages that we need : 

    * pip install paho-mqtt
    * pip install python-telegram-bot-raw --upgrade

Android APP setup : 
Just put apk into your android device .

    * MQTT_in0.apk

We use supervisor to automatically execute our mqtt_receiver.py or you could directly use python interpreter to do it.

    * sudo apt-get install supervisor 
    * sudo nano /etc/supervisor/conf.d/mqtt.conf
    * sudo chmod 775 mqtt.conf
    * sudo supervisorctl update
    * sudo supervisorctl start mqtt
    
    # sudo python3 mqtt_receiver.py

