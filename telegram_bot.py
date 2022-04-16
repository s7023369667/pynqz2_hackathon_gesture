import requests,pyimgur

class telegram_bot():
    def __init__(self,chat_id,token):
        self.chat_id = chat_id
        self.token = token
    def send_message(self,mes):
        method = 'sendMessage'
        response = requests.post(
            url='https://api.telegram.org/bot{0}/{1}'.format(self.token, method),
            data={'chat_id': self.chat_id, 'text': mes}
        ).json()
    def send_photo(self,res):
        PATH = f'./pictures/{res}.png'
        files = {'photo':open(PATH,'rb')}
        method = "sendPhoto"
        response = requests.post(f'https://api.telegram.org/bot{self.token}/{method}?chat_id={self.chat_id}',files=files)


# if __name__ == '__main__':
    # token = 'xxx'
    # chat_id = xxx
    # tb = telegram_bot(1963689302,'1916008529:AAGydfJQXNZtHuVFt63ahXSZJcIjPa8ZNWg')
    # tb.send_photo(5)
    # tb.send_message(5)
