import ast
import sys
from pathlib import Path

TARGET_DIR = Path("src/with_harness")


def check_architecture() -> list[str]:
    violations: list[str] = []

    for py_file in TARGET_DIR.glob("*.py"):
        if py_file.name == "__init__.py":
            continue

        source = py_file.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(py_file))

        # Regra 1: Eventos devem ser dataclasses frozen=True
        if py_file.name == "events.py":
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    is_frozen = any(
                        isinstance(dec, ast.Call)
                        and getattr(dec.func, "id", "") == "dataclass"
                        and any(
                            kw.arg == "frozen" and getattr(kw.value, "value", False) is True
                            for kw in dec.keywords
                        )
                        for dec in node.decorator_list
                    )
                    if not is_frozen:
                        violations.append(
                            f"[{py_file.name}:{node.lineno}] Evento '{node.name}' deve usar @dataclass(frozen=True)."
                        )

        # Regra 2: CartController não pode importar Invoice ou Inventory
        if py_file.name == "cart_stream.py":
            for node in ast.walk(tree):
                if isinstance(node, (ast.Import, ast.ImportFrom)):
                    module_name = getattr(node, "module", "") or ""
                    names = [alias.name for alias in node.names]
                    if "consumers" in module_name or any(
                        n in ("ReactiveInvoice", "ReactiveInventory") for n in names
                    ):
                        violations.append(
                            f"[{py_file.name}:{node.lineno}] Acoplamento proibido: produtor importando consumidor."
                        )

        # Regra 3: Consumidores não podem chamar .on_next() (encapsulamento do Sink)
        if py_file.name == "consumers.py":
            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                    if node.func.attr == "on_next":
                        violations.append(
                            f"[{py_file.name}:{node.lineno}] Violação de Sink: consumidor não pode chamar '.on_next()'."
                        )

        # Regra 4: Proibir try/except imperativo dentro de consumers.py (usar ops.catch)[cite: 45]
        if py_file.name == "consumers.py":
            for node in ast.walk(tree):
                if isinstance(node, ast.Try):
                    violations.append(
                        f"[{py_file.name}:{node.lineno}] Uso de 'try/except' em fluxo reativo. Utilize 'ops.catch'."
                    )

    return violations


if __name__ == "__main__":
    errors = check_architecture()
    if errors:
        print("❌ VIOLAÇÕES ARQUITETURAIS DETECTADAS:")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)
    print("✅ Validação arquitetural (AST) aprovada com 0 violações.")