import os
import subprocess

def run_cyclictest(output_file, duration=100000):
    command = [
        "sudo", "cyclictest",
        f"-l{duration}", "-m", "-Sp90", "-i200", "-h400", "-q"
    ]
    with open(output_file, "w") as f:
        subprocess.run(command, stdout=f)

def prepare_histogram(output_file, histogram_prefix, cores):
    with open("histogram", "w") as histogram:
        subprocess.run(["grep", "-v", "-e", "^#", "-e", "^$", output_file], stdout=histogram)
    for core in range(1, cores + 1):
        column = core + 1
        histogram_file = f"{histogram_prefix}{core}"
        with open(histogram_file, "w") as core_file:
            subprocess.run(["cut", f"-f1,{column}", "histogram"], stdout=core_file)

def main():
    output_file = "output"
    histogram_prefix = "histogram"
    cores = os.cpu_count()

    run_cyclictest(output_file)
    prepare_histogram(output_file, histogram_prefix, cores)

if __name__ == "__main__":
    main()
