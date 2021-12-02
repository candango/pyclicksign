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
from cartola import fs
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


@when("File is created at {path}")
def step_file_create_at(context, path):
    real_directory = get_absolute_path(path)
    context.tester.assertTrue(os.path.isdir(real_directory))
    context.tester.assertTrue(os.access(real_directory, os.W_OK))


@given("File for {index} exists at {path}")
def step_file_for_exists_at(context, index, path):
    real_account_path = get_absolute_path(path)
    context.tester.assertTrue(os.path.exists(real_account_path))
    context.tester.assertTrue(os.path.isfile(real_account_path))
    setattr(context, index, fs.read(real_account_path))


@given("Endereço do arquivo {file_index} existe em {path}")
def step_file_for_exists_at(context, file_index, path):
    real_file_path = get_absolute_path(path)
    context.tester.assertTrue(os.path.exists(real_file_path))
    context.tester.assertTrue(os.path.isfile(real_file_path))
    setattr(context, file_index, real_file_path)


@then("File at {path} removed")
def step_file_at_removed(context, path):
    real_path = get_absolute_path(path)
    context.tester.assertTrue(os.path.exists(real_path))
    context.tester.assertTrue(os.path.isfile(real_path))
    os.remove(real_path)
    context.tester.assertFalse(os.path.exists(real_path))
