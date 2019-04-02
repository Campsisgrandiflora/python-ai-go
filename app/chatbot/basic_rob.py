from chatterbot import ChatBot

# Create a new chat bot named Charlie
# chatbot = ChatBot(
#     'Charlie',
#     trainer='chatterbot.trainers.ListTrainer'
# )

# chatbot.train([
#     "Hi, can I help you?",
#     "Sure, I'd like to book a flight to Iceland.",
#     "Your flight has been booked."
# ])

# Get a response to the input text 'How are you?'
# response = chatbot.get_response('how are you?')


class myChat():
    def __init__(self):
        self.chatbot = ChatBot(
            'ai',
            trainer='chatterbot.trainers.ListTrainer'
        )

    def get_response(self, info):
        # 返回信息
        return str(self.chatbot.get_response(info))


chat = myChat()
# chat.chatbot.train([
#     "Hi, can I help you?",
#     "Sure, I'd like to book a flight to Iceland.",
#     "Your flight has been booked."
# ]
# )

# chat.chatbot.train([
#     "如何修改密码？",
#     "进入个人主页后在左侧面板找到“修改密码”，输入旧密码和新密码即可完成密码修改。",
# ]
# )

# print(chat.get_response("如何修改密码"))
