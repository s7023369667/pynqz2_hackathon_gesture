# This is a sample Python script.
import telegram
import requests
import time
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    id = "1928130820"
    b_id = '1963689302' 
    group_id = '-1001588931917'
    token = "1997238109:AAFrdEtGSNVzYvX_9JDvuK9C_5o6My7qjto"

    bot = telegram.Bot(token=('1997238109:AAFrdEtGSNVzYvX_9JDvuK9C_5o6My7qjto'))


    message = bot.send_message(chat_id=id, text='woo hoo!')
    photo = bot.send_photo(chat_id=id, photo = 'https://i.imgur.com/1IeKIPu.png')
    time.sleep(2)
    bot.delete_message(chat_id=id, message_id=photo.message_id)
    bot.delete_message(chat_id=id, message_id=message.message_id)
    #print(photo)


