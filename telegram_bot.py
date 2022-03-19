import time,telegram
CHAT_ID = **********
TOKEN = **********
class telegrambot():
    def __init__(self):
        token = TOKEN
        self.bot = telegram.Bot(token=token)

    def send_message(self,message):
        mes = self.bot.send_message(chat_id=CHAT_ID,text=message)
        return mes.message_id

    def send_photo(self,res):
        imgur = {7:'https://imgur.com/5KtIeQ2',8:'https://imgur.com/Ysrw1cF',
                 9:'https://imgur.com/prMcssG',10:'https://imgur.com/DAnNdDj',
                11:'https://imgur.com/Q91py1u'}
        photo = self.bot.send_photo(chat_id=CHAT_ID,photo=imgur[res])
        self.del_message(photo.message_id)

    def del_message(self,del_id):
        time.sleep(2)
        self.bot.delete_message(chat_id=CHAT_ID, message_id=del_id)

if __name__ == '__main__':
    tb = telegrambot()
    tb.send_photo(11)
    id=tb.send_message(11)
    tb.del_message(id)

