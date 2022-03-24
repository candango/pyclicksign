# Copyright 2021-2022 Flávio Gonçalves Garcia
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
from tornado import escape
import logging

logger = logging.getLogger(__name__)


@when("Cadastramos signatario com nome {nome} e email {email}")
@async_run_until_complete
async def step_enviamos_arquivo_por_upload(context, nome, email):
    context.signatarios = getattr(context, "signatarios", [])
    signatario_criado = False
    try:
        result = await context.protocol.create_signer(
            "email",
            name=nome,
            email=email,
            has_documentation=False
        )
        if result.code in [200, 201]:
            context.signatarios.append(escape.json_decode(result.body))
            signatario_criado = True
        else:
            logger.error(result.body)
    except HTTPError as e:
        print(e)
        logger.error(e)
    except Exception as e:
        print(e)
        logger.error(e)
    context.tester.assertTrue(signatario_criado)


@when("Adicionamos signatários ao documento válido")
@async_run_until_complete
async def step_enviamos_arquivo_por_upload(context):
    documento = escape.json_decode(context.documento_valido)
    signatarios = escape.json_decode(context.signatarios)
    context.lists = []
    try:
        for signatario in signatarios:
            result = await context.protocol.create_list(
                documento['document']['key'],
                signatario['signer']['key'],
            )
            if result.code in [200, 201]:
                context.lists.append(escape.json_decode(result.body))
            else:
                logger.error(result.body)
        print(context.lists)
    except HTTPError as e:
        print(e)
        logger.error(e)
    except Exception as e:
        print(e)
        logger.error(e)


@when("Solicitamos assinaturas dos signatarios por email")
@async_run_until_complete
async def step_solicitamos_assinaturas_signatarios_email(context):
    context.notifications = []
    try:
        for list in context.lists:
            result = await context.protocol.notify_by_email(
                list['list']['request_signature_key'],
                message="Por favor assine o documento."
            )
            print(result)
            if result.code in [200, 201]:
                context.notifications.append(escape.json_decode(result.body))
            else:
                logger.error(result.body)
        print(context.notifications)
    except HTTPError as e:
        print(e)
        logger.error(e)
    except Exception as e:
        print(e)
        logger.error(e)


@then("Signatários foram criados com sucesso")
def step_resposta_envio_por_upload_valida(context):
    context.tester.assertEqual(len(context.signatarios), 2)


@then("Listas foram criados com sucesso")
def step_resposta_envio_por_upload_valida(context):
    context.tester.assertEqual(len(context.lists), 2)
