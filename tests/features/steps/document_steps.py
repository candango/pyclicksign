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

from behave import given, when, then, step
from behave.api.async_step import async_run_until_complete
from tornado.httpclient import HTTPError
import logging

logger = logging.getLogger(__name__)


@when("Enviamos arquivo {file_index} por upload")
@async_run_until_complete
async def step_enviamos_arquivo_por_upload(context, file_index):
    successful = False
    file_path = getattr(context, file_index)
    try:
        result = await context.protocol.upload_file(file_path=file_path)
        print(result.body)
        successful = True
    except HTTPError as e:
        print(e)
        logger.error(e)
    except Exception as e:
        print(e)
        logger.error(e)
    context.tester.assertTrue(successful)