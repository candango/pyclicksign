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

Feature: Criar um documento para assinatura
  # Used to point service url's based on resource and action

  Scenario: Criar documento via upload

    Given Arquivo de sample_pdf_file existe em sandbox/sample-pdf-file.pdf
    When Enviamos arquivo sample_pdf_file por upload
    Then Resposta do envio por upload é valida
      And Podemos converter documento_valido de dict para texto
      And Arquivo de documento_valido é criado com sucesso em sandbox/documento_valido.txt
