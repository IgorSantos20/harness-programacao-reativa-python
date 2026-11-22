# Diretrizes de Desenvolvimento para Agentes de IA

Você está operando em um repositório governado por um **Harness Arquitetural** focado em **Programação Reativa e Orientada a Eventos (EDA)**.

## Fluxo Obrigatório de Trabalho
1. Leia `ARCHITECTURE.md` antes de escrever qualquer código.
2. Todo código de domínio deve ser implementado em `src/with_harness/`.
3. Após gerar ou modificar arquivos, execute obrigatoriamente:
   `python harness/run_harness.py`
4. Se o Harness reportar violações arquiteturais, erros de lint ou falhas de teste, corrija o código autonomamente até obter saída `EXIT_CODE=0` antes de encerrar a tarefa.

## Proibições Estritas
- **PROIBIDO** acoplamento direto entre módulos de domínio (ex: `Cart` importando ou invocando métodos de `Invoice` ou `Inventory`).
- **PROIBIDO** mutação de estado compartilhado fora de streams observáveis[cite: 14, 21, 45].
- **PROIBIDO** uso de `try/except` genérico dentro de fluxos assíncronos; utilize operadores reativos de tratamento de erro (`catch`, `retry`).
- **OBRIGATÓRIO** que eventos sejam estruturas de dados imutáveis (`@dataclass(frozen=True)`).