# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals

import pytest
import re
import vcr

from telebot import TeleBot

my_vcr = vcr.VCR(
    cassette_library_dir='tests/cassettes',
    # record_mode='all',
    record_mode='once',
    match_on=['uri', 'method'],
)


class TestTelebot:

    def setup(self):
        self.app = TeleBot(__name__)

    def teardown(self):
        self.app = None

    def test_no_config(self):
        ''' Verify polling can't start without api_key set.

        '''
        pytest.raises(ValueError, self.app.poll)

    def test_parrot_registered(self):
        ''' Verify route decorator registers within the update rules.

        '''
        @self.app.route('(?!/).+')
        def parrot(message):
            return "testing {}".format(message)

        assert len(self.app.update_rules) == 1
        assert self.app.update_rules[0]['rule'] == re.compile('(?!/).+')
        assert self.app.update_rules[0]['endpoint'] is None
        assert self.app.update_rules[0]['options'] == {}
        assert self.app.update_rules[0]['view_func']('it') == "testing it"

    @my_vcr.use_cassette('telegram.yaml')
    def test_start(self):
        self.app.config['api_key'] = '123:abc'
        self.app._start()

        assert self.app.whoami == {
            'first_name': 'Test-Bot',
            'id': 123,
            'username': 'TestBot',
        }

    @my_vcr.use_cassette('telegram.yaml')
    def test_start_existing(self):
        ''' Make sure start doesn't override whoami when previously set.

        '''
        self.app.config['api_key'] = '123:abc'
        self.app.whoami = {'id': 111}
        self.app._start()

        assert self.app.whoami == {'id': 111}

    @my_vcr.use_cassette('telegram.yaml')
    def test_parrot_app(self):
        test_messages = []

        @self.app.route('/command ?(.*)')
        def example_command(message, cmd):
            chat_dest = message['chat']['id']
            msg = "Command Received: {}".format(cmd)

            self.app.send_message(chat_dest, msg)
            test_messages.append([message, cmd, chat_dest, msg])

        @self.app.route('(?!/).+')
        def parrot(message):
            chat_dest = message['chat']['id']
            user_msg = message['text']

            msg = "Parrot Says: {}".format(user_msg)
            self.app.send_message(chat_dest, msg)
            test_messages.append([message, chat_dest, msg])

        self.app.config['api_key'] = '123:abc'
        pytest.raises(ValueError, self.app.poll, debug=True)
        assert test_messages == [
            [
                {
                    'chat': {
                        'first_name': 'Test',
                        'id': 8282,
                        'last_name': 'User',
                        'type': 'private',
                        'username': 'TestUser',
                    },
                    'date': 1462057648,
                    'from': {
                        'first_name': 'Test',
                        'id': 8282,
                        'last_name': 'User',
                        'username': 'TestUser',
                    },
                    'message_id': 73,
                    'text': 'Test 1',
                },
                8282,
                'Parrot Says: Test 1',
            ],
            [
                {
                    'chat': {
                        'first_name': 'Test',
                        'id': 8282,
                        'last_name': 'User',
                        'type': 'private',
                        'username': 'TestUser',
                    },
                    'date': 1462057662,
                    'entities': [
                        {'length': 8, 'offset': 0, 'type': 'bot_command'},
                    ],
                    'from': {
                        'first_name': 'Test',
                        'id': 8282,
                        'last_name': 'User',
                        'username': 'TestUser',
                    },
                    'message_id': 75,
                    'text': '/command test',
                },
                'test',
                8282,
                'Command Received: test',
            ],
            [
                {
                    'chat': {
                        'first_name': 'Test',
                        'id': 8282,
                        'last_name': 'User',
                        'type': 'private',
                        'username': 'TestUser',
                    },
                    'date': 1462057676,
                    'from': {
                        'first_name': 'Test',
                        'id': 8282,
                        'last_name': 'User',
                        'username': 'TestUser',
                    },
                    'message_id': 77,
                    'text': 'End test',
                },
                8282,
                'Parrot Says: End test'
            ],
        ]

if __name__ == '__main__':
    pytest.main()
