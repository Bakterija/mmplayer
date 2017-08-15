from __future__ import print_function
from kivy.properties import BooleanProperty, StringProperty, ListProperty
from kivy.network.urlrequest import UrlRequest
from kivy.event import EventDispatcher
from kivy.logger import Logger
from functools import partial
from kivy.clock import Clock
import traceback
import json


class RemoteClient(EventDispatcher):
    state = StringProperty('disconnected')
    _ip_addr = ListProperty(['', ''])
    _app_addr = StringProperty()
    _waiting_update = BooleanProperty(False)
    _server_data_index = -1

    def __init__(self, remote_control, **kwargs):
        self.register_event_type('on_connect_success')
        self.register_event_type('on_connect_fail')
        self.register_event_type('on_disconnect')
        self.register_event_type('on_send_fail')
        self.register_event_type('on_new_data')
        self.register_event_type('on_update_fail')
        super(RemoteClient, self).__init__(**kwargs)
        self.remote_control = remote_control

    def connect(self, ip_addr, passwd=None, port='5000'):
        if self.state == 'disconnected':
            self.state = 'connecting'
            self._trystate = {
                'http': {'done': False, 'success': False},
                'https': {'done': False, 'success': False}
            }
            self._ip_addr = [ip_addr, port]
            url_https = 'https://%s:%s/' % (ip_addr, port)
            url_http = 'http://%s:%s/' % (ip_addr, port)

            success_partial = partial(
                self._on_try_connect, 'http', ip_addr, port, True)
            fail_partial = partial(
                self._on_try_connect, 'http', ip_addr, port, False)
            req = UrlRequest(
                url_http, on_success=success_partial,
                on_redirect=success_partial, on_failure=fail_partial,
                on_error=fail_partial, verify=False)

            success_partial = partial(
                self._on_try_connect, 'https', ip_addr, port, True)
            fail_partial = partial(
                self._on_try_connect, 'https', ip_addr, port, False)
            req = UrlRequest(
                url_https, on_success=success_partial,
                on_redirect=success_partial, on_failure=fail_partial,
                on_error=fail_partial, verify=False)

            ret = '# RemoteClient: Trying %s:%s/ with http and https' % (ip_addr, port)
        else:
            ret = '# RemoteClient: Already connected, disconnect first'
        return ret

    def _on_try_connect(self, protocol, ip_addr, port, is_success, *args):
        if ip_addr == self._ip_addr[0] and port == self._ip_addr[1]:
            ts = self._trystate
            ts[protocol]['done'] = True
            ts[protocol]['success'] = is_success
            ts[protocol]['result'] = str(args)
            if ts['https']['done'] and ts['http']['done']:
                self._on_try_end(ip_addr, port)

    def _on_try_end(self, ip_addr, port):
        if self.state == 'connecting':
            ts = self._trystate
            if ts['https']['success'] or ts['http']['success']:
                if ts['https']['success']:
                    self._app_addr = 'https://%s:%s/' % (ip_addr, port)
                else:
                    self._app_addr = 'http://%s:%s/' % (ip_addr, port)
                self.state = 'connected'
                self.dispatch('on_connect_success')
            else:
                self._app_addr = ''
                self._ip_addr = ['', '']
                self.state = 'disconected'
                self.dispatch('on_connect_fail')
                Logger.info(
                    'RemoteClient: connection failed with results: %s %s' % (
                        (ts['https']['result'], ts['http']['result'])
                    )
                )

    def get_server_data_index(self, on_success, on_fail):
        url = '%s/get_log_len'  % (self._app_addr)
        req = UrlRequest(url, on_success=on_success,
                         on_redirect=on_success, on_failure=on_fail,
                         on_error=on_fail, verify=False)

    def send(self, text):
        ret = ''
        if self.state == 'connected':
            url = '%s/handle_input' % (self._app_addr)
            headers = {'Content-Type' : 'application/json'}
            data = json.dumps({'data': text})
            fail_partial = partial(self.dispatch, 'on_send_fail')
            req = UrlRequest(
                url, on_failure=fail_partial, on_error=fail_partial,
                verify=False, req_headers=headers, req_body=data)
        else:
            ret = '# Not connected'
        return ret

    def disconect(self):
        if self.state in ('connected', 'connecting'):
            self.state = 'disconnected'

    def on_state(self, _, value):
        if value == 'connected':
            Clock.schedule_interval(self.update, 0.15)
        elif value == 'disconnected':
            Clock.unschedule(self.update)

    def update(self, dt):
        if self._server_data_index == -1:
            self.get_server_data_index(
                lambda *a: setattr(self, '_server_data_index', int(a[1])),
                lambda *a: Logger.info(' '.join(
                    'RemoteClient: failed to get server data index',
                    'trying again'))
            )
        elif self._waiting_update:
            pass
        else:
            url = '%s/get_logs_after/%s' % (
                self._app_addr, self._server_data_index)
            self._waiting_update = True
            req = UrlRequest(
                url, on_success=self._on_update_success,
                on_redirect=self._on_update_success,
                on_failure=self._on_update_fail,
                on_error=self._on_update_fail, verify=False)

    def _on_update_success(self, _, result):
        result = json.loads(result)
        for x in result:
            self._server_data_index += 1
            x['text_raw'] = 'remote: %s' % (x['text_raw'])
            self.dispatch('on_new_data', x)
        self._waiting_update = False

    def _on_update_fail(self, _, response):
        self.dispatch('on_update_fail')
        self._waiting_update = False

    def on_new_data(self, data):
        pass

    def on_update_fail(self):
        pass

    def on_connect_success(self):
        pass

    def on_connect_fail(self):
        pass

    def on_disconnect(self):
        pass

    def on_send_fail(self, _, value):
        pass
