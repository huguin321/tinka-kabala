from pathlib import Path

ROOT = Path(r"D:\Tinka\TnkIntellij")
OUTPUT = ROOT / "codigo_fuente.txt"

IGNORE_DIRS = {".idea", ".venv", "__pycache__", ".git", "output"}
IGNORE_FILES = {OUTPUT.name}


def should_skip(path: Path) -> bool:
    return any(part in IGNORE_DIRS for part in path.parts) or path.name in IGNORE_FILES


# 🔥 LECTOR INTELIGENTE (SOLUCIÓN AL PROBLEMA)
def read_file_smart(path: Path) -> str:
    encodings = ["utf-8", "utf-8-sig", "cp1252", "latin-1"]

    for enc in encodings:
        try:
            return path.read_text(encoding=enc)
        except UnicodeDecodeError:
            continue

    # último recurso
    return path.read_text(encoding="utf-8", errors="replace")


files = sorted(
    [p for p in ROOT.rglob("*.py") if not should_skip(p)],
    key=lambda p: str(p).lower()
)

with OUTPUT.open("w", encoding="utf-8", newline="\n") as out:
    for file_path in files:
        rel = file_path.relative_to(ROOT)

        out.write(f"\n{'=' * 80}\n")
        out.write(f"{rel}\n")
        out.write(f"{'=' * 80}\n\n")

        # 🔥 AQUÍ ESTÁ EL CAMBIO CLAVE
        content = read_file_smart(file_path)
        out.write(content)

        out.write("\n")

print(f"Generado: {OUTPUT}")
