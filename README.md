# Harness para Agentes de IA — Programação Reativa / Orientada a Eventos (Python)

Projeto desenvolvido para a disciplina de **Paradigmas de Linguagens de Programação** (UFAL — Campus Arapiraca), baseado nos conceitos de **Programação Reativa** e **Orientação a Eventos** apresentados pelo Prof. Thiago de Sales, D.Sc.

## Visão Geral

Na abordagem imperativa/passiva tradicional, um módulo tende a alterar outro diretamente ou depender de chamadas remotas e controle manual de estado, o que aumenta o acoplamento e a complexidade conforme o sistema cresce. Na **Programação Reativa**, o foco está no **fluxo de dados** e na **propagação automática de mudanças**: o módulo alterado emite eventos em um fluxo (*Data Stream*), e os módulos observadores reagem automaticamente.

Este repositório apresenta:
1. Um núcleo reativo simples em Python (`ControladorFluxo` e `Fluxo`, com `ouvir`, `filtrar` e `mapear`).
2. Um exemplo de domínio com `Produto`, `Carrinho` e `Fatura`, onde a `Fatura` observa o fluxo do `Carrinho` sem chamadas imperativas diretas entre eles.
3. Um validador arquitetural (`validar_arquitetura.py`) e testes automatizados (`testar_reativo.py`) que compõem a base do **Harness** para orientar e fiscalizar agentes de IA.

## Estrutura do Projeto

- `reativo.py`: implementação de `ControladorFluxo` e `Fluxo` (emissão de dados/erros e operadores `filtrar` e `mapear`).
- `dominio.py`: modelos `Produto`, `Carrinho` (emissor via `fluxo_carrinho`) e `Fatura` (observador que recalcula o total automaticamente).
- `validar_arquitetura.py`: análise estática com `ast` para verificar regras arquiteturais reativas e retornar código de saída não zero em caso de violação.
- `testar_reativo.py`: suíte de testes com `unittest` cobrindo o fluxo do carrinho/fatura, operadores, propagação de erro e o validador arquitetural.

## Como Executar e Testar

No terminal, acesse a pasta do projeto e execute:

```bash
python dominio.py
python -m unittest discover -v
python validar_arquitetura.py
