import subprocess
import sys
from pathlib import Path

# Define the scripts to run in order
scripts = [
    "src/process_returns.py",
    "src/prep_model.py",
    "src/run_model.py"
]

def main():
    for script in scripts:
        print(f"Running {script}...")
        result = subprocess.run([sys.executable, script], capture_output=True, text=True)
        print(result.stdout)
        if result.returncode != 0:
            print(f"Error running {script}:")
            print(result.stderr)
            sys.exit(result.returncode)
    print("\nPipeline completed successfully.")

if __name__ == "__main__":
    main()
