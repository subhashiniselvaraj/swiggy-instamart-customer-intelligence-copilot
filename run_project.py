
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent

SCRIPTS = [
    "generate_data.py",
    "customer_segmentation.py",
    "triage.py",
    "policy_rag.py",
]


def main():
    for script in SCRIPTS:
        script_path = ROOT / script

        if not script_path.exists():
            print(f"ERROR: Could not find {script_path}")
            sys.exit(1)

        print(f"\n{'=' * 55}")
        print(f"Running {script}")
        print("=" * 55)

        result = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=ROOT,
            check=False,
        )

        if result.returncode != 0:
            print(f"\nERROR: {script} failed. Please check the message above.")
            sys.exit(result.returncode)

    print("\nAll four project scripts completed successfully!")
    print("Check the outputs folder for the generated results.")


if __name__ == "__main__":
    main()
