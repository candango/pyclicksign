# Copyright 2021-2022 Flavio Garcia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from . import get_version
import base64
from cartola import fs
import copy
from firenado import get_version as firenado_get_version
from firenado.tornadoweb import get_request
import logging
import magic
import os
from peasant import get_version as peasant_get_version
from peasant.client import AsyncPeasant, PeasantTransport
from tornado import version
from tornado import escape
from tornado.httputil import urlencode
from tornado.httpclient import AsyncHTTPClient, HTTPClientError, HTTPResponse
from uuid import uuid4
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class ClicksignApiTransport(PeasantTransport):

    def __init__(self, **kwargs):
        super(ClicksignApiTransport, self).__init__()
        self._client = AsyncHTTPClient()
        self._access_token = kwargs.get("access_token")
        self._bastion_address = kwargs.get("address",
                                           "app.clicksign.com")
        if "https://" not in  self._bastion_address:
            self._bastion_address = "https://%s" % self._bastion_address
        self._directory = None
        self.user_agent = ("PyClicksign/%s Peasant/%s Firenado/%s "
                           "Tornado/%s" %
                           (
                               get_version(),
                               peasant_get_version(),
                               firenado_get_version(),
                               version
                           ))
        self._basic_headers = {
            'User-Agent': self.user_agent
        }

    async def get(self, path, **kwargs) -> HTTPResponse:
        headers = kwargs.get('headers')
        request = get_request(path)
        print(path)
        if headers:
            request.headers.update(headers)
        return await self._client.fetch(request)

    async def head(self, path, **kwargs):
        headers = kwargs.get('headers')
        request = get_request(path, method="HEAD")
        _headers = copy.deepcopy(self._basic_headers)
        if headers:
            _headers.update(headers)
        request.headers.update(_headers)
        return await self._client.fetch(request)

    async def post(self, path, **kwargs):
        headers = kwargs.get('headers')
        form_data = kwargs.get("form_data", {})
        request = get_request(path, method="POST")
        _headers = copy.deepcopy(self._basic_headers)
        if headers:
            _headers.update(headers)
        request.headers.update(_headers)
        if "Content-Type" in request.headers and request.headers[
           'Content-Type'] == "application/json":
            form_data = escape.json_encode(form_data)
        request.body = form_data
        try:
            result = await self._client.fetch(request)
        except HTTPClientError as error:
            result = error.response
        return result

    def set_directory(self):
        self.peasant.directory_cache = {
            "account_test": "%s/%s?access_token=%s" % (
                self._bastion_address,
                "api/v1/accounts",
                self._access_token
            ),
            "upload_document": "%s/%s?access_token=%s" % (
                self._bastion_address,
                "api/v1/documents",
                self._access_token
            )
        }
        return

    async def new_nonce(self):
        url = (await self.peasant.directory())['security']['newNonce']
        response = await self.head(url)
        return response.headers.get("Replay-Nonce")

    async def user_auth(self, **kwargs):
        headers = kwargs.get("headers", {})
        headers['nonce'] = await self.new_nonce()
        url = (await self.peasant.directory())['security']['userAuth']
        form_data = kwargs.get("form_data", {})
        response = await self.post(url, form_data=form_data, headers=headers)
        return response

    async def knock(self, **kwargs):
        headers = kwargs.get("headers", {})
        headers['nonce'] = await self.new_nonce()
        url = (await self.peasant.directory())['peasant']['knock']
        response = await self.head(url, headers=headers)
        return response

    async def register(self, **kwargs):
        headers = kwargs.get("headers", {})
        form_data = kwargs.get("form_data", {})
        headers['nonce'] = await self.new_nonce()
        url = (await self.peasant.directory())['peasant']['register']
        response = await self.post(url, form_data=form_data, headers=headers)
        return response

    async def device_ping(self, payload, **kwargs):
        headers = kwargs.get("headers", {})
        form_data = {'payload': kwargs.get("form_data", payload)}
        headers['nonce'] = await self.new_nonce()
        url = (await self.peasant.directory())['device']['ping']
        response = await self.post(url, form_data=form_data, headers=headers)
        return response


class ClicksignPeasant(AsyncPeasant):

    def __init__(self, transport: ClicksignApiTransport):
        super(ClicksignPeasant, self).__init__(transport)

    @property
    def component(self):
        return self._component

    @property
    def user_agent(self):
        return self.transport.user_agent

    async def test_account(self) -> HTTPResponse:
        directory = await self.directory()
        return await self.transport.get(directory['account_test'])

    async def upload_file(self, **kwargs) -> HTTPResponse:
        path = kwargs.get("path")
        file_path = kwargs.get("file_path")
        mime = None
        file_base46 = None
        document_data = {
            'document': {
                'path': "/%s",
                'content_base64': "data:%s;base64,%s",
                'deadline_at': "%s-03:00",
                'auto_close': True,
                'locale': "pt-BR",
                'sequence_enabled': False
            }
        }

        if os.path.exists(file_path):
            with magic.Magic(flags=magic.MAGIC_MIME_TYPE) as m:
                mime = m.id_filename(file_path)

            file_base46 = base64.b64encode(fs.read(file_path, True))
        document_data['document']['content_base64'] = "data:%s;base64,%s" % (
            mime, file_base46.decode())
        document_data['document']['path'] = "/%s.pdf" % uuid4()
        document_data['document']['deadline_at'] = "%s-03:00" % (
                datetime.now() + timedelta(days=1)
        ).strftime("%Y-%m-%dT%H:%M:%S")
        directory = await self.directory()
        headers = {'Content-Type': "application/json"}
        return await self.transport.post(
            directory['upload_document'], headers=headers,
            form_data=document_data)
        # payload = self.component.encrypt(
        #     escape.json_encode(kwargs.get("payload")).encode()
        # )
        # headers = self.prepare_knock(**kwargs)
        # return await self.transport.device_ping(payload, headers=headers)
