import re
import requests
import time


class TeleBot(object):

    def __init__(self, import_name):
        self.import_name = import_name
        self.update_rules = list()
        self.config = dict(
            api_key=None,
            requests_kwargs=dict(
                timeout=60,
            ),
        )
        self.offset = 0
        self.whoami = None

    def add_update_rule(self, rule, endpoint=None, view_func=None, **options):
        self.update_rules.append(dict(
            rule=re.compile(rule),
            endpoint=endpoint,
            view_func=view_func,
            options=dict(**options),
        ))

    def route(self, rule, **options):
        """A decorator that is used to register a view function for a
        given URL rule.  This does the same thing as :meth:`add_url_rule`
        but is intended for decorator usage::
            @app.route('/')
            def index():
                return 'Hello World'
        For more information refer to :ref:`url-route-registrations`.
        :param rule: the URL rule as string
        :param endpoint: the endpoint for the registered URL rule.  Flask
                         itself assumes the name of the view function as
                         endpoint
        :param options: the options to be forwarded to the underlying
                        :class:`~werkzeug.routing.Rule` object.  A change
                        to Werkzeug is handling of method options.  methods
                        is a list of methods this rule should be limited
                        to (``GET``, ``POST`` etc.).  By default a rule
                        just listens for ``GET`` (and implicitly ``HEAD``).
                        Starting with Flask 0.6, ``OPTIONS`` is implicitly
                        added and handled by the standard request handling.
        """
        def decorator(f):
            endpoint = options.pop('endpoint', None)
            self.add_update_rule(rule, endpoint, f, **options)
            return f
        return decorator

    def process_update(self, update):
        self.offset = max(self.offset, update.get('update_id', 0)) + 1

        for x in self.update_rules:
            # TODO: Find a good pattern to detect each type and process
            #       accordingly.
            if 'message' in update and 'text' in update['message'] and \
                    x['rule'].match(update['message']['text']):
                m = x['rule'].match(update['message']['text'])
                x['view_func'](update['message'],
                               *m.groups(),
                               **m.groupdict())

    def process_updates(self, updates):
        if updates.get('ok', False) is True:
            for msg in updates['result']:
                self.process_update(msg)

    def _start(self):
        '''Requests bot information based on current api_key, and sets
        self.whoami to dictionary with username, first_name, and id of the
        configured bot.

        '''
        if self.whoami is None:
            me = self.get_me()
            if me.get('ok', False):
                self.whoami = me['result']
            else:
                raise ValueError("Bot Cannot request information, check "
                                 "api_key")

    def poll(self, offset=None, poll_timeout=600, cooldown=60, debug=False):
        '''These should also be in the config section, but some here for
        overrides

        '''
        if self.config['api_key'] is None:
            raise ValueError("config api_key is undefined")

        if offset or self.config.get('offset', None):
            self.offset = offset or self.config.get('offset', None)

        self._start()

        while True:
            try:
                response = self.get_updates(poll_timeout, self.offset)
                if response.get('ok', False) is False:
                    raise ValueError(response['error'])
                else:
                    self.process_updates(response)
            except Exception as e:
                print("Error: Unknown Exception")
                print(e)
                if debug:
                    raise e
                else:
                    time.sleep(cooldown)

    def listen(self):
        raise NotImplemented

    def _bot_cmd(self, method, endpoint, *args, **kwargs):
        base_api = "https://api.telegram.org/bot{api_key}/{endpoint}"
        endpoint = base_api.format(api_key=self.config['api_key'],
                                   endpoint=endpoint)

        try:
            response = method(endpoint,
                              data=kwargs.get('data', None),
                              params=kwargs.get('params', {}),
                              **self.config['requests_kwargs'])

            if response.status_code != 200:
                raise ValueError('Got unexpected response. ({}) - {}'.
                                 format(response.status_code, response.text))

            return response.json()
        except Exception as e:
            return {
                'ok': False,
                'error': str(e),
            }

    def get_me(self):
        '''A simple method for testing your bot's auth token. Requires no
        parameters. Returns basic information about the bot in form of a `User
        object.

        '''
        return self._bot_cmd(requests.get, 'getMe')

    def send_message(self, chat_id, text):
        data = dict(
            chat_id=chat_id,
            text=text,
        )

        return self._bot_cmd(requests.post, 'sendMessage', data=data)

    def forward_message(self):
        raise NotImplemented("forward_message needs work")

    def send_photo(self):
        raise NotImplemented("send_photo needs work")

    def send_audio(self):
        raise NotImplemented("send_audio needs work")

    def send_document(self):
        raise NotImplemented("send_document needs work")

    def send_sticker(self):
        raise NotImplemented("send_sticker needs work")

    def send_video(self):
        raise NotImplemented("send_video needs work")

    def send_location(self):
        raise NotImplemented("send_location needs work")

    def send_chat_action(self):
        raise NotImplemented("send_chat_action needs work")

    def get_user_profile_photos(self):
        raise NotImplemented("get_user_profile_photos needs work")

    def get_updates(self, timeout=0, offset=None):
        params = dict(
            timeout=timeout,
            offset=offset,
        )
        return self._bot_cmd(requests.get, 'getUpdates', params=params)

    def set_webhook(self):
        raise NotImplemented("set_webhook needs work")
