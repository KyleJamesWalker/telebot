telebot
-------

A Telegram bot library, with simple route decorators.

Currently a work in progress, doesn't do much now, but will register and send messages.

Example Setup
^^^^^^^^^^^^^
::

 from telebot import TeleBot

 app = TeleBot(__name__)


 @app.route('/command ?(.*)')
 def example_command(message, cmd):
     chat_dest = message['chat']['id']
     msg = "Command Recieved: {}".format(cmd)

     app.send_message(chat_dest, msg)


 @app.route('(?!/).+')
 def parrot(message):
    chat_dest = message['chat']['id']
    user_msg = message['text']

    msg = "Parrot Says: {}".format(user_msg)
    app.send_message(chat_dest, msg)


 if __name__ == '__main__':
     app.config['api_key'] = 'xxxxxxxx:enterYourBotKeyHereToTest'
     app.poll(debug=True)
