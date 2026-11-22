# Regras Arquiteturais — Backend Reativo

1. **Inversão de Controle via Data Streams**:
   - O módulo produtor emite eventos através de um `Subject` / `Sink` sem conhecer seus consumidores[cite: 22, 24, 48].
   - Módulos consumidores (`Invoice`, `Inventory`) se inscrevem (`subscribe`) nos fluxos filtrados ou transformados (`map`, `filter`) e são responsáveis por sua própria auto-atualização[cite: 21, 28, 33, 44].
2. **Imutabilidade de Eventos**:
   - Todos os eventos trafegados nos streams devem ser classes `@dataclass(frozen=True)`.
3. **Encapsulamento do Sink**:
   - Nenhum consumidor externo pode chamar `.on_next()` diretamente no `Subject` de outro domínio. O produtor deve expor apenas a propriedade `Observable` (somente leitura)[cite: 24, 26].
4. **Pureza dos Operadores**:
   - Funções passadas para `.pipe(ops.map(...), ops.filter(...))` devem ser puras, sem efeitos colaterais (*side-effects* ficam restritos ao `.subscribe()`)[cite: 44, 45].