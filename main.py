"""
main.py — QuantumCrypt Lab
Application entry point.

Run with:
    python main.py
"""

import sys
import os


def check_dependencies():
    """Check that required packages are installed and give helpful errors."""
    missing = []

    try:
        import customtkinter  # noqa: F401
    except ImportError:
        missing.append("customtkinter")

    try:
        from Crypto.Cipher import AES  # noqa: F401
    except ImportError:
        missing.append("pycryptodome")

    try:
        # pyrefly: ignore [missing-import]
        import qiskit  # noqa: F401
    except ImportError:
        missing.append("qiskit")

    try:
        import qiskit_aer  # noqa: F401
    except ImportError:
        missing.append("qiskit-aer")

    if missing:
        print("=" * 60)
        print("QuantumCrypt Lab — Missing Dependencies")
        print("=" * 60)
        print(f"\nMissing packages: {', '.join(missing)}")
        print("\nFix — Option 1 (install globally):")
        print("  pip install -r requirements.txt")
        print("\nFix — Option 2 (use the virtual environment):")
        print("  venv\\Scripts\\python.exe main.py")
        print("\nFix — Option 3 (activate venv first, then run):")
        print("  venv\\Scripts\\Activate.ps1")
        print("  python main.py")
        print()
        sys.exit(1)


def _try_relaunch_with_venv():
    """
    If running with the system Python and the venv exists, automatically
    re-launch using the venv's Python interpreter.
    """
    venv_python = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "venv", "Scripts", "python.exe"
    )
    current_exe = os.path.abspath(sys.executable)

    if os.path.isfile(venv_python) and not current_exe.startswith(
        os.path.dirname(os.path.abspath(venv_python))
    ):
        # We are NOT running from the venv — try to relaunch with it
        import subprocess
        try:
            result = subprocess.run(
                [venv_python, __file__] + sys.argv[1:],
                check=False
            )
            sys.exit(result.returncode)
        except Exception:
            pass  # Fall through to normal dependency check


def main():
    # First try to auto-relaunch using the venv if we're on system Python
    _try_relaunch_with_venv()

    # If we're already in the venv (or relaunch failed), check deps normally
    check_dependencies()

    # Defer heavy imports until after dependency check
    from ui import QuantumCryptLabApp

    app = QuantumCryptLabApp()
    app.mainloop()


if __name__ == "__main__":
    main()
