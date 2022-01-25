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

Feature: Adicionando signatários a um documento existente
  # Used to point service url's based on resource and action

  Scenario: Criar signatários

    Given Arquivo de documento_valido existe em sandbox/documento_valido.txt
      And Ler dados de documento_valido sucedeu
    When Cadastramos signatario com nome Signatario Um e email signatario1@test.ts
      And Cadastramos signatario com nome Signatario Dois e email signatario2@test.ts
    Then Signatários foram criados com sucesso
      And Podemos converter signatarios de dict para texto
      And Arquivo de signatarios é criado com sucesso em sandbox/signatarios.txt

  Scenario: Adicionar signatários ao documento

    Given Arquivo de documento_valido existe em sandbox/documento_valido.txt
      And Ler dados de documento_valido sucedeu
      And Arquivo de signatarios existe em sandbox/signatarios.txt
      And Ler dados de signatarios sucedeu
    When Adicionamos signatários ao documento válido