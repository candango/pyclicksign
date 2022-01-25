# -*- coding: UTF-8 -*-
#
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
import sys

from cartola import sysexits
from behave import fixture, use_fixture
import os
from pyclicksign.protocol import ClicksignApiTransport, ClicksignPeasant
from unittest.case import TestCase

CLICKSIGN_ACCESS_TOKEN = os.getenv("CLICKSIGN_ACCESS_TOKEN")


@fixture
def protocol(context, timeout=1, **kwargs):
    if not CLICKSIGN_ACCESS_TOKEN:
        sys.exit(sysexits.EX_CANNOT_EXECUTE)
    transport = ClicksignApiTransport(
        address="sandbox.clicksign.com",
        access_token=CLICKSIGN_ACCESS_TOKEN
    )
    context.protocol = ClicksignPeasant(transport)
    yield context.protocol


@fixture
def tester(context, timeout=1, **kwargs):
    context.tester = TestCase()
    yield context.tester


@fixture
def sandbox_path(context, timeout=1, **kwargs):
    context.sandbox_path = os.path.realpath(
        os.path.join(os.path.dirname(__file__), "..", "sandbox")
    )
    yield context.sandbox_path


def before_all(context):
    use_fixture(protocol, context)
    use_fixture(sandbox_path, context)
    use_fixture(tester, context)
