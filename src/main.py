import csv
import json
import matplotlib.pyplot as plt
import time
from pathlib import Path
from algorithms.fifo import fifo_scheduling
from algorithms.spt import spt_scheduling
from algorithms.edd import edd_scheduling

from evaluation.evaluator import (
    calculate_makespan,
    evaluate_schedule,
    calculate_machine_utilization,
    validate_schedule_operations
)
from evaluation.evaluator import (
    calculate_makespan,
    evaluate_schedule,
    calculate_machine_utilization,
    validate_schedule_operations,
    validate_job_precedence
)
from evaluation.evaluator import (
    calculate_makespan,
    evaluate_schedule,
    calculate_machine_utilization,
    validate_schedule_operations,
    validate_job_precedence,
    validate_machine_overlap
)

# ==========================================
# STEP 1: LOAD BENCHMARK DATA
# ==========================================

file_path = (
    Path(__file__).parent.parent
    / "Data"
    / "ft06_6_jobs_6_resources.json"
)

with open(file_path, "r") as file:
    data = json.load(file)

resources = data["resources"]
jobs = data["jobs"]

print("========== BENCHMARK INFORMATION ==========")
print("Benchmark: ft06")
print("Machines:", len(resources))
print("Jobs:", len(jobs))

total_operations = sum(
    len(job["operations"]) for job in jobs
)

print("Total operations:", total_operations)


# ==========================================
# STEP 2: DISPLAY JOB 0 OPERATIONS
# ==========================================

print("\n========== JOB 0 OPERATIONS ==========")

job_0 = jobs[0]

for operation in job_0["operations"]:

    print(
        "Operation:", operation["index"],
        "| Duration:", operation["duration"],
        "| Machine:", operation["resource"]
    )


# ==========================================
# STEP 3: FIFO SCHEDULING
# ==========================================

# STEP 18.1: GENERATE ARTIFICIAL DUE DATES


# ==========================================
# STEP 4: SPT SCHEDULING
# ==========================================

# STEP 18.2: EDD SCHEDULING ALGORITHM



# ==========================================
# STEP 5: RUN FIFO AND SPT
# ==========================================

fifo_schedule = fifo_scheduling(jobs, resources)
spt_schedule = spt_scheduling(jobs, resources)
edd_schedule = edd_scheduling(jobs, resources)
# Save original FT06 schedules for validation
fifo_ft06_schedule = fifo_schedule.copy()
spt_ft06_schedule = spt_schedule.copy()
edd_ft06_schedule = edd_schedule.copy()


# STEP 18.3: RUN EDD ON FT06

edd_schedule = edd_scheduling(jobs, resources)
edd_makespan = max(operation["end"] for operation in edd_schedule)

print("\nEDD Schedule:")
print(edd_schedule)

print("EDD Makespan:", edd_makespan)

# ==========================================
# STEP 6: DISPLAY FIFO RESULTS
# ==========================================

print("\n========== FIFO RESULTS ==========")

for item in fifo_schedule:

    print(
        f"Job {item['job']} | "
        f"Operation {item['operation']} | "
        f"Machine {item['machine']} | "
        f"Start {item['start']} | "
        f"End {item['end']}"
    )

fifo_makespan = max(
    item["end"] for item in fifo_schedule
)

print("\nTotal scheduled operations:", len(fifo_schedule))
print("FIFO Makespan:", fifo_makespan)


# ==========================================
# STEP 7: DISPLAY SPT RESULTS
# ==========================================

print("\n========== SPT RESULTS ==========")

for item in spt_schedule:

    print(
        f"Job {item['job']} | "
        f"Operation {item['operation']} | "
        f"Machine {item['machine']} | "
        f"Start {item['start']} | "
        f"End {item['end']}"
    )

spt_makespan = max(
    item["end"] for item in spt_schedule
)

print("\nTotal scheduled operations:", len(spt_schedule))
print("SPT Makespan:", spt_makespan)


# ==========================================
# STEP 8: COMPARE FIFO AND SPT
# ==========================================

print("\n========== FIFO VS SPT COMPARISON ==========")

print("FIFO Makespan:", fifo_makespan)
print("SPT Makespan:", spt_makespan)

if fifo_makespan > spt_makespan:

    improvement = (
        (fifo_makespan - spt_makespan)
        / fifo_makespan
    ) * 100

    print(f"SPT improvement: {improvement:.2f}%")

elif spt_makespan > fifo_makespan:

    print("FIFO produced a lower makespan.")

else:

    print("Both algorithms produced the same makespan.")

def validate_schedule(schedule, jobs, resources):

    errors = []

    # Check that every operation is scheduled exactly once
    expected = {
        (job["id"], op["index"])
        for job in jobs
        for op in job["operations"]
    }

    actual = [
        (item["job"], item["operation"])
        for item in schedule
    ]

    if set(actual) != expected or len(actual) != len(expected):
        errors.append("Missing or duplicate operations")

    # Check job operation order
    for job in jobs:

        job_id = job["id"]

        job_operations = sorted(
            [item for item in schedule if item["job"] == job_id],
            key=lambda item: item["operation"]
        )

        for i in range(1, len(job_operations)):

            previous = job_operations[i - 1]
            current = job_operations[i]

            if previous["end"] > current["start"]:
                errors.append(
                    f"Job {job_id}: operation order violation"
                )

    # Check machine conflicts
    for resource in resources:

        machine_id = resource["id"]

        machine_operations = sorted(
            [item for item in schedule if item["machine"] == machine_id],
            key=lambda item: item["start"]
        )

        for i in range(1, len(machine_operations)):

            previous = machine_operations[i - 1]
            current = machine_operations[i]

            if previous["end"] > current["start"]:
                errors.append(
                    f"Machine {machine_id}: overlapping operations"
                )

    if errors:
        print("Schedule is INVALID:")
        for error in errors:
            print(error)
        return False

    print("Schedule is VALID!")
    return True


# Validate both schedules
print("\n========== VALIDATION ==========")

print("FIFO:")
fifo_valid = validate_schedule(fifo_schedule, jobs, resources)

print("\nSPT:")
spt_valid = validate_schedule(spt_schedule, jobs, resources)

print("\n========== PROGRAM COMPLETED ==========")


# ==========================================
# STEP 9: FIND ALL BENCHMARK FILES
# ==========================================

data_folder = Path(__file__).parent.parent / "Data"

benchmark_files = sorted(data_folder.glob("*.json"))

print("\n========== AVAILABLE BENCHMARKS ==========")

print("Total benchmark files:", len(benchmark_files))

for file in benchmark_files:
    print(file.name)

# ==========================================
# STEP 10: BATCH SCHEDULING
# ==========================================

print("\n========== BATCH SCHEDULING RESULTS ==========")

print(
    f"{'Benchmark':<40}"
    f"{'Jobs':>6}"
    f"{'Machines':>10}"
    f"{'Ops':>8}"
    f"{'FIFO':>10}"
    f"{'SPT':>10}"
)

print("-" * 84)

for benchmark_file in benchmark_files:

    # Load benchmark
    with open(benchmark_file, "r") as file:
        benchmark_data = json.load(file)

    benchmark_jobs = benchmark_data["jobs"]
    benchmark_resources = benchmark_data["resources"]

    # Run FIFO
    fifo_result = fifo_scheduling(
        benchmark_jobs,
        benchmark_resources
    )

    # Run SPT
    spt_result = spt_scheduling(
        benchmark_jobs,
        benchmark_resources
    )

    
    # Calculate makespan using central evaluator
    fifo_evaluation = evaluate_schedule(fifo_result)
    spt_evaluation = evaluate_schedule(spt_result)

    fifo_ms = fifo_evaluation["makespan"]
    spt_ms = spt_evaluation["makespan"]


    # Count operations
    total_ops = sum(
        len(job["operations"])
        for job in benchmark_jobs
    )

    # Print result
    print(
        f"{benchmark_file.stem:<40}"
        f"{len(benchmark_jobs):>6}"
        f"{len(benchmark_resources):>10}"
        f"{total_ops:>8}"
        f"{fifo_ms:>10}"
        f"{spt_ms:>10}"
    )

print("\n========== BATCH COMPLETED ==========")
print("Benchmarks processed:", len(benchmark_files))


# ==========================================
# STEP 11: EXPORT RESULTS TO CSV
# ==========================================

results_file = data_folder / "batch_results.csv"

with open(results_file, "w", newline="") as file:

    writer = csv.writer(file)

    # CSV header
    writer.writerow([
        "Benchmark",
        "Jobs",
        "Machines",
        "Operations",
        "FIFO_Makespan",
        "SPT_Makespan"
    ])

    # Process each benchmark
    for benchmark_file in benchmark_files:

        with open(benchmark_file, "r") as json_file:
            benchmark_data = json.load(json_file)

        benchmark_jobs = benchmark_data["jobs"]
        benchmark_resources = benchmark_data["resources"]

        fifo_result = fifo_scheduling(
            benchmark_jobs,
            benchmark_resources
        )

        spt_result = spt_scheduling(
            benchmark_jobs,
            benchmark_resources
        )

        
        fifo_evaluation = evaluate_schedule(fifo_result)
        spt_evaluation = evaluate_schedule(spt_result)

        fifo_ms = fifo_evaluation["makespan"]
        spt_ms = spt_evaluation["makespan"]


        total_ops = sum(
            len(job["operations"])
            for job in benchmark_jobs
        )

        writer.writerow([
            benchmark_file.stem,
            len(benchmark_jobs),
            len(benchmark_resources),
            total_ops,
            fifo_ms,
            spt_ms
        ])

print("\nCSV successfully saved!")
print("File location:", results_file)


# ==========================================
# STEP 12: STATISTICAL ANALYSIS
# ==========================================

print("\n========== STATISTICAL ANALYSIS ==========")

csv_file = data_folder / "batch_results.csv"

fifo_wins = 0
spt_wins = 0
equal_results = 0

fifo_total = 0
spt_total = 0

improvement_total = 0

with open(csv_file, "r") as file:

    reader = csv.DictReader(file)

    for row in reader:

        fifo_ms = int(row["FIFO_Makespan"])
        spt_ms = int(row["SPT_Makespan"])

        fifo_total += fifo_ms
        spt_total += spt_ms

        if fifo_ms < spt_ms:
            fifo_wins += 1

        elif spt_ms < fifo_ms:
            spt_wins += 1

        else:
            equal_results += 1

        # SPT improvement percentage
        improvement = (
            (fifo_ms - spt_ms) / fifo_ms
        ) * 100

        improvement_total += improvement

total_benchmarks = (
    fifo_wins + spt_wins + equal_results
)

average_fifo = fifo_total / total_benchmarks
average_spt = spt_total / total_benchmarks

average_improvement = (
    improvement_total / total_benchmarks
)

print("Total benchmarks:", total_benchmarks)

print("\n========== ALGORITHM WINS ==========")

print("FIFO wins:", fifo_wins)
print("SPT wins:", spt_wins)
print("Equal results:", equal_results)
  
print("\n========== AVERAGE MAKESPAN ==========")

print(f"FIFO average: {average_fifo:.2f}")
print(f"SPT average: {average_spt:.2f}")

print("\n========== SPT IMPROVEMENT ==========")

print(
    f"Average improvement: "
    f"{average_improvement:.2f}%"
)

print("\n========== ANALYSIS COMPLETED ==========")


# ==========================================
# STEP 13: GENERATE RESEARCH GRAPHS
# ==========================================

# Graph 1: Average Makespan Comparison

algorithms = ["FIFO", "SPT"]
average_makespans = [average_fifo, average_spt]

plt.figure(figsize=(8, 5))

plt.bar(algorithms, average_makespans)

plt.title("Average Makespan: FIFO vs SPT")
plt.xlabel("Scheduling Algorithm")
plt.ylabel("Average Makespan")

plt.tight_layout()

plt.savefig(data_folder / "average_makespan.png")

plt.close()


# Graph 2: Algorithm Wins

algorithm_names = ["FIFO", "SPT", "Equal"]
wins = [fifo_wins, spt_wins, equal_results]

plt.figure(figsize=(8, 5))

plt.bar(algorithm_names, wins)

plt.title("Algorithm Performance Across 81 Benchmarks")
plt.xlabel("Result")
plt.ylabel("Number of Benchmarks")

plt.tight_layout()

plt.savefig(data_folder / "algorithm_wins.png")

plt.close()

print("\nGraphs successfully generated!")


# ==========================================
# STEP 14: MAKESPAN COMPARISON ALL BENCHMARKS
# ==========================================

benchmark_names = []
fifo_values = []
spt_values = []

with open(csv_file, "r") as file:

    reader = csv.DictReader(file)

    for row in reader:

        benchmark_names.append(row["Benchmark"])
        fifo_values.append(int(row["FIFO_Makespan"]))
        spt_values.append(int(row["SPT_Makespan"]))


plt.figure(figsize=(20, 7))

plt.plot(
    benchmark_names,
    fifo_values,
    label="FIFO",
    marker="o",
    markersize=3
)

plt.plot(
    benchmark_names,
    spt_values,
    label="SPT",
    marker="o",
    markersize=3
)

plt.title("FIFO vs SPT Makespan Across 81 Benchmarks")
plt.xlabel("Benchmark")
plt.ylabel("Makespan")

plt.xticks(rotation=90, fontsize=7)

plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()

plt.savefig(
    data_folder / "all_benchmark_comparison.png",
    dpi=300
)

plt.close()

print("All benchmark comparison graph generated!")


# ==========================================
# STEP 15: JOB COUNT VS MAKESPAN
# ==========================================

job_counts = {}

with open(csv_file, "r") as file:

    reader = csv.DictReader(file)

    for row in reader:

        jobs_count = int(row["Jobs"])
        fifo_ms = int(row["FIFO_Makespan"])
        spt_ms = int(row["SPT_Makespan"])

        if jobs_count not in job_counts:

            job_counts[jobs_count] = {
                "fifo": [],
                "spt": []
            }

        job_counts[jobs_count]["fifo"].append(fifo_ms)
        job_counts[jobs_count]["spt"].append(spt_ms)


# Calculate averages for each job count

job_numbers = sorted(job_counts.keys())

fifo_averages = []
spt_averages = []

for jobs_count in job_numbers:

    fifo_avg = (
        sum(job_counts[jobs_count]["fifo"])
        / len(job_counts[jobs_count]["fifo"])
    )

    spt_avg = (
        sum(job_counts[jobs_count]["spt"])
        / len(job_counts[jobs_count]["spt"])
    )

    fifo_averages.append(fifo_avg)
    spt_averages.append(spt_avg)


# Create graph

plt.figure(figsize=(10, 6))

plt.plot(
    job_numbers,
    fifo_averages,
    marker="o",
    label="FIFO"
)

plt.plot(
    job_numbers,
    spt_averages,
    marker="o",
    label="SPT"
)

plt.title("Job Count vs Average Makespan")
plt.xlabel("Number of Jobs")
plt.ylabel("Average Makespan")

plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()

plt.savefig(
    data_folder / "job_count_vs_makespan.png",
    dpi=300
)

plt.close()

print("Job count scaling graph generated!")


# ==========================================
# STEP 16: MACHINE UTILIZATION ANALYSIS
# ==========================================

fifo_utilization_results = []
spt_utilization_results = []

for benchmark_file in benchmark_files:

    # Load benchmark
    with open(benchmark_file, "r") as file:
        benchmark_data = json.load(file)

    benchmark_jobs = benchmark_data["jobs"]
    benchmark_resources = benchmark_data["resources"]

    # Run scheduling algorithms
    fifo_schedule = fifo_scheduling(
        benchmark_jobs,
        benchmark_resources
    )

    spt_schedule = spt_scheduling(
        benchmark_jobs,
        benchmark_resources
    )

    # Calculate makespan
    fifo_makespan = max(
        item["end"] for item in fifo_schedule
    )

    spt_makespan = max(
        item["end"] for item in spt_schedule
    )

    # Calculate busy time for each machine
    fifo_machine_busy = {
        resource["id"]: 0
        for resource in benchmark_resources
    }

    spt_machine_busy = {
        resource["id"]: 0
        for resource in benchmark_resources
    }

    for item in fifo_schedule:

        duration = item["end"] - item["start"]

        fifo_machine_busy[item["machine"]] += duration

    for item in spt_schedule:

        duration = item["end"] - item["start"]

        spt_machine_busy[item["machine"]] += duration

    # Calculate utilization for each machine
    fifo_machine_utilization = [
        (busy_time / fifo_makespan) * 100
        for busy_time in fifo_machine_busy.values()
    ]

    spt_machine_utilization = [
        (busy_time / spt_makespan) * 100
        for busy_time in spt_machine_busy.values()
    ]

    # Average utilization across machines
    fifo_average_utilization = (
        sum(fifo_machine_utilization)
        / len(fifo_machine_utilization)
    )

    spt_average_utilization = (
        sum(spt_machine_utilization)
        / len(spt_machine_utilization)
    )

    fifo_utilization_results.append(
        fifo_average_utilization
    )

    spt_utilization_results.append(
        spt_average_utilization
    )


# Overall average utilization
overall_fifo_utilization = (
    sum(fifo_utilization_results)
    / len(fifo_utilization_results)
)

overall_spt_utilization = (
    sum(spt_utilization_results)
    / len(spt_utilization_results)
)

print("\n========== MACHINE UTILIZATION ==========")

print(
    f"FIFO Average Utilization: "
    f"{overall_fifo_utilization:.2f}%"
)

print(
    f"SPT Average Utilization: "
    f"{overall_spt_utilization:.2f}%"
)


# Create utilization graph
plt.figure(figsize=(8, 5))

plt.bar(
    ["FIFO", "SPT"],
    [
        overall_fifo_utilization,
        overall_spt_utilization
    ]
)

plt.title("Average Machine Utilization")
plt.xlabel("Scheduling Algorithm")
plt.ylabel("Utilization (%)")

plt.tight_layout()

plt.savefig(
    data_folder / "machine_utilization.png",
    dpi=300
)

plt.close()

print("Machine utilization graph generated!")


# ==========================================
# STEP 17: RUNTIME ANALYSIS
# ==========================================

fifo_runtimes = []
spt_runtimes = []

runtime_csv = data_folder / "runtime_results.csv"

with open(runtime_csv, "w", newline="") as file:

    writer = csv.writer(file)

    writer.writerow([
        "Benchmark",
        "FIFO_Runtime_ms",
        "SPT_Runtime_ms"
    ])

    for benchmark_file in benchmark_files:

        with open(benchmark_file, "r") as json_file:
            benchmark_data = json.load(json_file)

        benchmark_jobs = benchmark_data["jobs"]
        benchmark_resources = benchmark_data["resources"]

        # Measure FIFO runtime
        start = time.perf_counter()

        fifo_scheduling(
            benchmark_jobs,
            benchmark_resources
        )

        fifo_runtime = (
            time.perf_counter() - start
        ) * 1000

        # Measure SPT runtime
        start = time.perf_counter()

        spt_scheduling(
            benchmark_jobs,
            benchmark_resources
        )

        spt_runtime = (
            time.perf_counter() - start
        ) * 1000

        fifo_runtimes.append(fifo_runtime)
        spt_runtimes.append(spt_runtime)

        writer.writerow([
            benchmark_file.stem,
            fifo_runtime,
            spt_runtime
        ])


# Calculate average runtime

average_fifo_runtime = (
    sum(fifo_runtimes) / len(fifo_runtimes)
)

average_spt_runtime = (
    sum(spt_runtimes) / len(spt_runtimes)
)

print("\n========== RUNTIME ANALYSIS ==========")

print(
    f"FIFO Average Runtime: "
    f"{average_fifo_runtime:.4f} ms"
)

print(
    f"SPT Average Runtime: "
    f"{average_spt_runtime:.4f} ms"
)


# Runtime graph

plt.figure(figsize=(8, 5))

plt.bar(
    ["FIFO", "SPT"],
    [
        average_fifo_runtime,
        average_spt_runtime
    ]
)

plt.title("Average Scheduling Runtime")
plt.xlabel("Algorithm")
plt.ylabel("Runtime (ms)")

plt.tight_layout()

plt.savefig(
    data_folder / "runtime_comparison.png",
    dpi=300
)

plt.close()

print("Runtime analysis completed!")


# STEP 19.1: EDD BATCH SCHEDULING

edd_results = []

for benchmark_file in benchmark_files:
    with open(benchmark_file, "r") as json_file:
        benchmark_data = json.load(json_file)

    benchmark_jobs = benchmark_data["jobs"]
    benchmark_resources = benchmark_data["resources"]

    edd_schedule = edd_scheduling(
        benchmark_jobs,
        benchmark_resources
    )

    edd_evaluation = evaluate_schedule(edd_schedule)
    edd_makespan = edd_evaluation["makespan"]

    edd_results.append({
        "Benchmark": benchmark_file.stem,
        "EDD_Makespan": edd_makespan
    })

print("\n========== EDD BATCH RESULTS ==========")

for result in edd_results:
    print(
        result["Benchmark"],
        "| EDD Makespan:",
        result["EDD_Makespan"]
    )

print("\nEDD benchmarks processed:", len(edd_results))


# STEP 19.2: SAVE EDD RESULTS TO CSV

edd_csv = data_folder / "edd_results.csv"

with open(edd_csv, "w", newline="") as file:
    writer = csv.writer(file)

    writer.writerow(["Benchmark", "EDD_Makespan"])

    for result in edd_results:
        writer.writerow([
            result["Benchmark"],
            result["EDD_Makespan"]
        ])

print("\nEDD results CSV successfully saved!")
print("File location:", edd_csv)



# STEP 19.3: COMBINE FIFO, SPT AND EDD RESULTS

combined_csv = data_folder / "combined_results.csv"

# Read existing FIFO and SPT results
fifo_spt_csv = data_folder / "batch_results.csv"

fifo_spt_data = {}

with open(fifo_spt_csv, "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        fifo_spt_data[row["Benchmark"]] = row

with open(combined_csv, "w", newline="") as file:
    writer = csv.writer(file)

    writer.writerow([
        "Benchmark",
        "FIFO_Makespan",
        "SPT_Makespan",
        "EDD_Makespan"
    ])

    for edd in edd_results:
        benchmark = edd["Benchmark"]
        fifo_spt = fifo_spt_data[benchmark]

        writer.writerow([
            benchmark,
            fifo_spt["FIFO_Makespan"],
            fifo_spt["SPT_Makespan"],
            edd["EDD_Makespan"]
        ])

print("\nCombined results successfully saved!")
print("File location:", combined_csv)


# STEP 19.4: THREE ALGORITHMS COMPARISON GRAPH

combined_csv = data_folder / "combined_results.csv"

benchmarks = []
fifo_values = []
spt_values = []
edd_values = []

with open(combined_csv, "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        benchmarks.append(row["Benchmark"])
        fifo_values.append(int(row["FIFO_Makespan"]))
        spt_values.append(int(row["SPT_Makespan"]))
        edd_values.append(int(row["EDD_Makespan"]))

plt.figure(figsize=(16, 7))

plt.plot(benchmarks, fifo_values, label="FIFO")
plt.plot(benchmarks, spt_values, label="SPT")
plt.plot(benchmarks, edd_values, label="EDD")

plt.xlabel("Benchmark")
plt.ylabel("Makespan")
plt.title("FIFO vs SPT vs EDD - Benchmark Comparison")

plt.legend()
plt.xticks(rotation=90)
plt.grid(True)
plt.tight_layout()

graph_path = data_folder / "three_algorithm_comparison.png"
plt.savefig(graph_path)
plt.close()

print("\nThree algorithm comparison graph generated!")
print("Graph location:", graph_path)


# STEP 20.1: AVERAGE MAKESPAN OF THREE ALGORITHMS

combined_csv = data_folder / "combined_results.csv"

fifo_total = 0
spt_total = 0
edd_total = 0
benchmark_count = 0

with open(combined_csv, "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        fifo_total += int(row["FIFO_Makespan"])
        spt_total += int(row["SPT_Makespan"])
        edd_total += int(row["EDD_Makespan"])
        benchmark_count += 1

fifo_average = fifo_total / benchmark_count
spt_average = spt_total / benchmark_count
edd_average = edd_total / benchmark_count

print("\n========== STEP 20.1 RESULTS ==========")
print("Total Benchmarks:", benchmark_count)
print(f"FIFO Average Makespan: {fifo_average:.2f}")
print(f"SPT Average Makespan: {spt_average:.2f}")
print(f"EDD Average Makespan: {edd_average:.2f}")


# STEP 20.2: BEST ALGORITHM WINS ANALYSIS

fifo_wins = 0
spt_wins = 0
edd_wins = 0
ties = 0

with open(combined_csv, "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        fifo = int(row["FIFO_Makespan"])
        spt = int(row["SPT_Makespan"])
        edd = int(row["EDD_Makespan"])

        minimum = min(fifo, spt, edd)

        winners = 0

        if fifo == minimum:
            fifo_wins += 1
            winners += 1

        if spt == minimum:
            spt_wins += 1
            winners += 1

        if edd == minimum:
            edd_wins += 1
            winners += 1

        if winners > 1:
            ties += 1

print("\n========== STEP 20.2 RESULTS ==========")
print("FIFO Wins:", fifo_wins)
print("SPT Wins:", spt_wins)
print("EDD Wins:", edd_wins)
print("Benchmarks with Ties:", ties)


# STEP 20.3: IMPROVEMENT PERCENTAGE COMPARISON

spt_improvements = []
edd_improvements = []

with open(combined_csv, "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        fifo = int(row["FIFO_Makespan"])
        spt = int(row["SPT_Makespan"])
        edd = int(row["EDD_Makespan"])

        spt_improvement = ((fifo - spt) / fifo) * 100
        edd_improvement = ((fifo - edd) / fifo) * 100

        spt_improvements.append(spt_improvement)
        edd_improvements.append(edd_improvement)

average_spt_improvement = sum(spt_improvements) / len(spt_improvements)
average_edd_improvement = sum(edd_improvements) / len(edd_improvements)

print("\n========== STEP 20.3 RESULTS ==========")
print(f"SPT Improvement over FIFO: {average_spt_improvement:.2f}%")
print(f"EDD Improvement over FIFO: {average_edd_improvement:.2f}%")


# STEP 20.4: FINAL AVERAGE MAKESPAN GRAPH

algorithms = ["FIFO", "SPT", "EDD"]
average_makespans = [
    fifo_average,
    spt_average,
    edd_average
]

plt.figure(figsize=(8, 6))

bars = plt.bar(algorithms, average_makespans)

plt.xlabel("Scheduling Algorithm")
plt.ylabel("Average Makespan")
plt.title("Average Makespan Comparison - 81 Benchmarks")

plt.bar_label(bars, fmt="%.2f")
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()

final_graph = data_folder / "average_makespan_comparison.png"
plt.savefig(final_graph)
plt.close()

print("\nFinal average makespan graph generated!")
print("Graph location:", final_graph)

# STEP 23: Test Central Evaluator

print("\nSTEP 23: Testing Central Evaluator")

fifo_evaluation = evaluate_schedule(fifo_schedule)
spt_evaluation = evaluate_schedule(spt_schedule)
edd_evaluation = evaluate_schedule(edd_schedule)

print("FIFO Evaluation:", fifo_evaluation)
print("SPT Evaluation:", spt_evaluation)
print("EDD Evaluation:", edd_evaluation)


# STEP 25: Test Machine Utilization Evaluator

print("\nSTEP 25: Testing Machine Utilization Evaluator")

fifo_utilization = calculate_machine_utilization(
    fifo_schedule, resources
)

spt_utilization = calculate_machine_utilization(
    spt_schedule, resources
)

edd_utilization = calculate_machine_utilization(
    edd_schedule, resources
)

print(f"FIFO Utilization: {fifo_utilization:.2f}%")
print(f"SPT Utilization: {spt_utilization:.2f}%")
print(f"EDD Utilization: {edd_utilization:.2f}%")


# STEP 26: Testing Schedule Validation

print("\nSTEP 26: Testing Schedule Validation")

expected_operations = [
    (job["id"], operation["index"])
    for job in jobs
    for operation in job["operations"]
]


fifo_validation = validate_schedule_operations(
    fifo_ft06_schedule, expected_operations
)

spt_validation = validate_schedule_operations(
    spt_ft06_schedule, expected_operations
)

edd_validation = validate_schedule_operations(
    edd_ft06_schedule, expected_operations
)

print("FIFO Validation:", fifo_validation)
print("SPT Validation:", spt_validation)
print("EDD Validation:", edd_validation)


print("\nSTEP 27: Testing Job Precedence Validation")

fifo_precedence = validate_job_precedence(
    fifo_ft06_schedule, jobs
)

spt_precedence = validate_job_precedence(
    spt_ft06_schedule, jobs
)

edd_precedence = validate_job_precedence(
    edd_ft06_schedule, jobs
)

print("FIFO Precedence:", fifo_precedence)
print("SPT Precedence:", spt_precedence)
print("EDD Precedence:", edd_precedence)



print("\nSTEP 28: Testing Machine Overlap Validation")

fifo_overlap = validate_machine_overlap(fifo_ft06_schedule)
spt_overlap = validate_machine_overlap(spt_ft06_schedule)
edd_overlap = validate_machine_overlap(edd_ft06_schedule)

print("FIFO Machine Overlap:", fifo_overlap)
print("SPT Machine Overlap:", spt_overlap)
print("EDD Machine Overlap:", edd_overlap)


print("\nSTEP 29: Testing Central Evaluator")

expected_operations = [
    (job["id"], operation["index"])
    for job in jobs
    for operation in job["operations"]
]

fifo_evaluation = evaluate_schedule(
    fifo_ft06_schedule, jobs, expected_operations
)

spt_evaluation = evaluate_schedule(
    spt_ft06_schedule, jobs, expected_operations
)

edd_evaluation = evaluate_schedule(
    edd_ft06_schedule, jobs, expected_operations
)

print("FIFO Evaluation:", fifo_evaluation)
print("SPT Evaluation:", spt_evaluation)
print("EDD Evaluation:", edd_evaluation)
