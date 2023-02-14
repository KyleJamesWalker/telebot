Telebot
-------

Note: This is not `pyTelegramBotAPI <https://github.com/eternnoir/pyTelegramBotAPI>`_, but do to often confusion I have included
it within this package.  So if you accidentally install this instead of `pyTelegramBotAPI <https://github.com/eternnoir/pyTelegramBotAPI>`_
the examples, etc will still work.

This originally was telegram bot library, with simple route decorators, and will now
be imported as telebot_router, to separate `pyTelegramBotAPI <https://github.com/eternnoir/pyTelegramBotAPI>`_ and this package from
collision.

Currently a work in progress, doesn't do much now, but will register and send messages.

Example Setup
^^^^^^^^^^^^^
::

 from telebot_router import TeleBot

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
