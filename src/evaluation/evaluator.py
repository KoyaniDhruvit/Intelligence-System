
def calculate_makespan(schedule):
    if not schedule:
        return 0

    return max(operation["end"] for operation in schedule)



def evaluate_schedule(schedule, jobs=None, expected_operations=None):
    makespan = calculate_makespan(schedule)

    result = {
        "makespan": makespan,
        "total_operations": len(schedule)
    }

    if expected_operations is not None:
        result["operation_validation"] = validate_schedule_operations(
            schedule, expected_operations
        )

    if jobs is not None:
        result["precedence_validation"] = validate_job_precedence(
            schedule, jobs
        )

    result["machine_overlap_validation"] = validate_machine_overlap(
        schedule
    )

    return result


def calculate_machine_utilization(schedule, resources):
    makespan = calculate_makespan(schedule)

    if makespan == 0:
        return 0

    
    machine_ids = {
        operation["machine"]
        for operation in schedule
    }

    machine_busy_time = {
        machine: 0
        for machine in machine_ids
    }


    for operation in schedule:
        duration = operation["end"] - operation["start"]
        machine_busy_time[operation["machine"]] += duration

    machine_utilization = [
        (busy_time / makespan) * 100
        for busy_time in machine_busy_time.values()
    ]

    average_utilization = (
        sum(machine_utilization) / len(machine_utilization)
    )

    return average_utilization


def validate_schedule_operations(schedule, expected_operations):
    scheduled_operations = [
        (operation["job"], operation["operation"])
        for operation in schedule
    ]

    expected_set = set(expected_operations)
    scheduled_set = set(scheduled_operations)

    missing_operations = expected_set - scheduled_set
    duplicate_operations = (
        len(scheduled_operations) - len(scheduled_set)
    )
    unexpected_operations = scheduled_set - expected_set


    return {
        "valid": (
            len(missing_operations) == 0
            and duplicate_operations == 0
            and len(unexpected_operations) == 0
        ),
        "missing_operations": len(missing_operations),
        "duplicate_operations": duplicate_operations,
        "unexpected_operations": len(unexpected_operations)
    }

def validate_job_precedence(schedule, jobs):
    schedule_by_job = {}

    for operation in schedule:
        job_id = operation["job"]
        operation_id = operation["operation"]

        if job_id not in schedule_by_job:
            schedule_by_job[job_id] = {}

        schedule_by_job[job_id][operation_id] = operation

    violations = []

    for job in jobs:
        job_id = job["id"]
        operations = job["operations"]

        for i in range(1, len(operations)):
            previous_operation = schedule_by_job[job_id][i - 1]
            current_operation = schedule_by_job[job_id][i]

            if current_operation["start"] < previous_operation["end"]:
                violations.append({
                    "job": job_id,
                    "previous_operation": i - 1,
                    "current_operation": i
                })

    return {
        "valid": len(violations) == 0,
        "precedence_violations": len(violations)
    }


def validate_machine_overlap(schedule):
    machine_operations = {}

    for operation in schedule:
        machine = operation["machine"]

        if machine not in machine_operations:
            machine_operations[machine] = []

        machine_operations[machine].append(operation)

    violations = []

    for machine, operations in machine_operations.items():
        operations.sort(key=lambda operation: operation["start"])

        for i in range(1, len(operations)):
            previous_operation = operations[i - 1]
            current_operation = operations[i]

            if current_operation["start"] < previous_operation["end"]:
                violations.append({
                    "machine": machine,
                    "previous_job": previous_operation["job"],
                    "current_job": current_operation["job"]
                })

    return {
        "valid": len(violations) == 0,
        "machine_overlap_violations": len(violations)
    }
