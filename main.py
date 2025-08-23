import subprocess
import sys
from pathlib import Path

# Define the scripts to run in order
scripts = [
    ("src/process_returns.py", "Processing returns..."),
    ("src/prep_model.py", "Preparing model..."),
    ("src/run_model.py", "Running model..."),
    ("src/plot_results.py", "Plotting results..."),
    ("src/forecast.py", "Forecasting..."),
    ("src/plot_forecast.py", "Plotting forecast..."),
    ("src/backtest.py", "Running backtest..."),
    ("src/backtest_data.py", "Preparing backtest data...")
]

def main():
    for script in scripts:
        print(f"\n{script[1]}")
        result = subprocess.run([sys.executable, script[0]], capture_output=True, text=True)
        print(result.stdout)
        if result.returncode != 0:
            print(f"Error running {script}:")
            print(result.stderr)
            sys.exit(result.returncode)
    print("\nPipeline completed successfully.")

if __name__ == "__main__":
    main()