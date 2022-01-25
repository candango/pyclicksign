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
from cartola import fs
from tornado.escape import json_encode, json_decode
import os


def get_absolute_path(directory):
    return os.path.realpath(
        os.path.join(os.path.dirname(__file__), "..", "..", directory)
    )


def create_file(path, content, binary=False):
    real_path = get_absolute_path(path)
    fs.write(real_path, content, binary)
    os.chmod(real_path, 0o600)
    return real_path


@then("Podemos converter {index} de dict para texto")
def step_arquivo_criado_com_sucesso(context, index):
    data = getattr(context, index)
    setattr(context, index, json_encode(data))


@then("Podemos converter {index} de texto para dict")
def step_arquivo_criado_com_sucesso(context, index):
    data = getattr(context, index)
    setattr(context, index, json_decode(data))


@then("Arquivo de {index} é criado com sucesso em {path}")
def step_arquivo_criado_com_sucesso(context, index, path):
    data = getattr(context, index)
    if isinstance(data, dict):
        data = json_encode(data)
    if isinstance(data, str):
        data = data.encode()
    real_path = create_file(path, data, True)
    context.tester.assertTrue(os.path.exists(real_path))
    context.tester.assertTrue(os.path.isfile(real_path))


@given("Arquivo de {index} existe em {path}")
def step_arquivo_existe(context, index, path):
    real_path = get_absolute_path(path)
    context.tester.assertTrue(os.path.exists(real_path))
    context.tester.assertTrue(os.path.isfile(real_path))
    setattr(context, index, real_path)
    print(getattr(context, index))


@given("Ler dados de {index} sucedeu")
def step_arquivo_existe(context, index):
    real_path = getattr(context, index)
    setattr(context, index, fs.read(real_path))


@then("File at {path} removed")
def step_file_at_removed(context, path):
    real_path = get_absolute_path(path)
    context.tester.assertTrue(os.path.exists(real_path))
    context.tester.assertTrue(os.path.isfile(real_path))
    os.remove(real_path)
    context.tester.assertFalse(os.path.exists(real_path))
