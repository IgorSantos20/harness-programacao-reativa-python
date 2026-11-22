# Reactive AI Harness — Engenharia de Guardrails para Agentes de IA

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![ReactiveX](https://img.shields.io/badge/ReactiveX-RxPY-ff1744.svg)](https://rxpy.readthedocs.io/)
[![Linter: Ruff](https://img.shields.io/badge/linter-ruff-d7ff64.svg)](https://docs.astral.sh/ruff/)
[![Architecture: Event-Driven](https://img.shields.io/badge/architecture-EDA%20%2F%20Reactive-success.svg)](#)

Este repositório demonstra como construir um **Harness (arnês de engenharia determinístico)** para guiar, restringir e validar agentes de Inteligência Artificial na construção de sistemas backend baseados em **Programação Reativa e Orientada a Eventos (EDA)**.

O projeto compara lado a lado a mesma funcionalidade de backend (um fluxo de checkout de e-commerce: *Carrinho $\rightarrow$ Fatura $\rightarrow$ Estoque*) implementada **sem** e **com** a governança do Harness.

---

## Problema e Motivação

Quando solicitados a implementar regras de negócio sem restrições arquiteturais explícitas e verificáveis, agentes de IA tendem a gerar código **imperativo e fortemente acoplado** ("este módulo altera aquele módulo"):

```text
[Abordagem Imperativa / Passiva]
Cart.add_product() ──(chamada direta)──► Inventory.decrease_stock()
                   ──(chamada direta)──► Invoice.update_invoice()
```

Nesse modelo:
* O produtor (`Cart`) conhece e controla seus dependentes.
* Falhas em um módulo secundário quebram o fluxo principal.
* Adicionar um novo consumidor (ex.: auditoria, notificações, analytics) exige modificar o código do produtor.

Com o **Harness Reativo**, o agente é compelido a inverter o controle utilizando **Data Streams (Fluxos de Dados)** e o **Padrão Observer**:

```text
[Abordagem Reativa / Event-Driven]
                        ┌──► .pipe(map)    ──► ReactiveInvoice (auto-atualização)
CartController (Sink) ──┤
  (Observable Stream)   └──► .pipe(filter) ──► ReactiveInventory (auto-atualização)
```

---

## Estrutura do Repositório

```text
reactive-ai-harness/
├── AGENTS.md                        # Contrato de instruções e restrições operacionais para o Agente
├── ARCHITECTURE.md                  # Especificação formal das regras de arquitetura reativa
├── pyproject.toml                   # Configurações de linter (Ruff) e suíte de testes (Pytest)
├── README.md                        # Documentação geral do experimento e guia de execução
│
├── harness/                         # Núcleo de governança e validação automatizada
│   ├── __init__.py
│   ├── validator.py                 # Analisador estático via AST (bloqueia violações arquiteturais)
│   └── run_harness.py               # Pipeline orquestrador (Lint -> AST -> Testes)
│
├── src/
│   ├── without_harness/             # Cenário A: Implementação gerada livremente (Imperativa)
│   │   ├── __init__.py
│   │   └── checkout_imperative.py
│   │
│   └── with_harness/                # Cenário B: Implementação governada pelo Harness (Reativa)
│       ├── __init__.py
│       ├── events.py                # Contratos de eventos imutáveis (@dataclass(frozen=True))
│       ├── cart_stream.py           # Produtor / Controller que encapsula o Subject (Sink)
│       └── consumers.py             # Observadores desacoplados inscrevendo-se nos streams
│
└── tests/
    └── test_reactive_checkout.py    # Testes comportamentais, de imutabilidade e resiliência de stream
```

---

## Como o Harness Funciona

O Harness atua como um **ciclo fechado de feedback determinístico** para o agente de IA, composto por quatro camadas:

1. **Contexto Diretivo (`AGENTS.md` & `ARCHITECTURE.md`)**:
   Define o protocolo obrigatório de trabalho do agente antes de escrever código e estabelece as fronteiras do domínio.
2. **Análise Estática de Estilo e Tipagem (`Ruff`)**:
   Garante conformidade sintática, ordenação de imports e boas práticas modernas em Python.
3. **Validação Arquitetural por AST (`harness/validator.py`)**:
   Inspeciona a *Abstract Syntax Tree* (Árvore Sintática Abstrata) do código gerado para detectar violações semânticas que linters comuns ignoram:
   * **Regra 1 (Imutabilidade):** Todo evento em `events.py` deve utilizar `@dataclass(frozen=True)`.
   * **Regra 2 (Desacoplamento):** `cart_stream.py` é proibido de importar classes consumidoras (`ReactiveInvoice`, `ReactiveInventory`).
   * **Regra 3 (Encapsulamento do Sink):** Consumidores não podem invocar `.on_next()` diretamente; apenas o produtor emite sinais.
   * **Regra 4 (Tratamento de Erros Reativo):** Proíbe blocos `try/except` imperativos dentro dos fluxos de consumo, exigindo o uso de operadores reativos como `ops.catch`.
4. **Testes Comportamentais (`Pytest`)**:
   Valida a propagação assíncrona de eventos para múltiplos assinantes e a resiliência do fluxo frente a entradas inválidas (`on_error`).

---

## Comparativo Experimental: Sem Harness vs. Com Harness

Para avaliar a eficácia da arquitetura, a mesma tarefa de implementação e evolução (adicionar cálculo de fatura, baixa de estoque e resiliência a falhas) foi submetida a um agente de IA nos dois cenários:

| Métrica Avaliada | ❌ Sem Harness (`without_harness`) | ✅ Com Harness (`with_harness`) | Ganho de Engenharia |
| :--- | :---: | :---: | :--- |
| **Violações Arquiteturais** | **4 violações** (acoplamento direto entre módulos, mutação de estado compartilhado, ausência de streams) | **0 violações** (100% desacoplado via `Subject`/`Observable` e eventos imutáveis) | Bloqueio automático de código imperativo via AST antes de qualquer revisão. |
| **Erros de Execução / Regressão** | **3 erros** (exceções síncronas não tratadas derrubando o carrinho; risco de mutação de payload) | **0 erros** (isolamento de falhas por consumidor via `ops.catch` e payload imutável) | Erros capturados e autocorrigidos pelo agente no loop de execução. |
| **Intervenções Humanas** | **3 intervenções** (necessidade de solicitar refatoração para eventos, desacoplamento e tratamento de erro) | **0 intervenções** (agente lê `AGENTS.md`, executa `run_harness.py` e corrige falhas sozinho) | Redução a zero do esforço humano em revisões arquiteturais básicas. |
| **Extensibilidade (Novo Consumidor)** | Exige modificar a classe `Cart` (violando o princípio *Open/Closed*) | Zero alterações no `CartController`; basta inscrever um novo observador em `cart.stream` | Aderência nativa à arquitetura orientada a eventos. |

---

## Como Executar Localmente

### Pré-requisitos
* Python **3.12** ou superior
* Gerenciador de pacotes `pip`

### 1. Instalação das dependências

Clone o repositório e instale as bibliotecas necessárias (`reactivex`, `pytest` e `ruff`):

```bash
git clone https://github.com/seu-usuario/reactive-ai-harness.git
cd reactive-ai-harness

python -m venv .venv
source .venv/bin/activate  # No Windows: .venv\Scripts\activate

pip install reactivex pytest ruff
```

### 2. Executando o Pipeline Completo do Harness

Para rodar todas as barreiras de validação (Linter + AST Validator + Testes Unitários) em sequência:

```bash
python harness/run_harness.py
```

**Saída esperada em caso de conformidade (`EXIT_CODE=0`):**
```text
--- Executando: 1. Linter & Formatação (Ruff) ---
All checks passed!

--- Executando: 2. Validação Arquitetural (AST) ---
   Validação arquitetural (AST) aprovada com 0 violações.

--- Executando: 3. Testes Comportamentais (Pytest) ---
tests/test_reactive_checkout.py::test_event_immutability PASSED
tests/test_reactive_checkout.py::test_reactive_propagation_to_multiple_consumers PASSED
tests/test_reactive_checkout.py::test_stream_error_resilience PASSED

   Todas as barreiras do Harness foram satisfeitas.
```

### 3. Executando Etapas Individualmente (Opcional)

Caso deseje testar cada camada do Harness separadamente:

```bash
# Apenas validação arquitetural via AST
python harness/validator.py

# Apenas suíte de testes reativos
pytest -v

# Apenas verificação de lint
ruff check src/with_harness tests
```

---

## Testando o Harness na Prática com um Agente de IA

Para observar o Harness em ação com qualquer agente de codificação (Claude Code, Cursor, GitHub Copilot, Gemini CLI, etc.):

1. Peça ao agente: *"Leia `AGENTS.md` e adicione um novo consumidor `ReactiveAuditLogger` em `src/with_harness/consumers.py` que registre todas as compras acima de R$ 1.000,00."*
2. Observe o agente implementar o filtro (`ops.filter`), executar `python harness/run_harness.py`, detectar eventuais violações (como uso de `try/except` ou chamada indevida a `.on_next()`) e corrigir o próprio código até passar em todas as validações.