from chatbot import ChatBot


if __name__ == '__main__':
    ai = ChatBot()

    while True:
        user_input = input("user: ")
        ai.chat(user_input)
