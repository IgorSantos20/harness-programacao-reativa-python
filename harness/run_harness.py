import subprocess
import sys


def run_step(name: str, command: list[str]) -> bool:
    print(f"\n--- Executando: {name} ---")
    result = subprocess.run(command, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout.strip())
    if result.stderr:
        print(result.stderr.strip())
    return result.returncode == 0


def main() -> None:
    steps = [
        ("1. Linter & Formatação (Ruff)", ["ruff", "check", "src/with_harness", "tests"]),
        ("2. Validação Arquitetural (AST)", [sys.executable, "harness/validator.py"]),
        ("3. Testes Comportamentais (Pytest)", [sys.executable, "-m", "pytest", "-v"]),
    ]

    for name, cmd in steps:
        if not run_step(name, cmd):
            print(f"\nFALHA NO HARNESS NA ETAPA: {name}")
            print("Ação requerida: Corrija os apontamentos acima e re-execute o harness.")
            sys.exit(1)

    print("\n🎉 SUCESSO TOTAL: Todas as barreiras do Harness foram satisfeitas.")
    sys.exit(0)


if __name__ == "__main__":
    main()