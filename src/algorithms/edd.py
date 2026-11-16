
# EDD Scheduling Algorithm

def generate_due_dates(jobs):

    due_dates = {}

    for job in jobs:
        job_id = job["id"]

        total_processing_time = sum(
            operation["duration"]
            for operation in job["operations"]
        )

        due_dates[job_id] = total_processing_time

    return due_dates


def edd_scheduling(jobs, resources):

    due_dates = generate_due_dates(jobs)

    machine_ids = {
        operation["resource"]
        for job in jobs
        for operation in job["operations"]
    }

    resource_available = {
        machine: 0 for machine in machine_ids
    }

    job_available = {
        job["id"]: 0 for job in jobs
    }

    next_operation = {
        job["id"]: 0 for job in jobs
    }

    schedule = []

    while any(
        next_operation[job["id"]] < len(job["operations"])
        for job in jobs
    ):

        ready_jobs = [
            job for job in jobs
            if next_operation[job["id"]] < len(job["operations"])
        ]

        job = min(
            ready_jobs,
            key=lambda item: (
                due_dates[item["id"]],
                item["id"]
            )
        )

        job_id = job["id"]

        operation_index = next_operation[job_id]
        operation = job["operations"][operation_index]

        machine = operation["resource"]
        duration = operation["duration"]

        start = max(
            job_available[job_id],
            resource_available[machine]
        )

        end = start + duration

        schedule.append({
            "job": job_id,
            "operation": operation_index,
            "machine": machine,
            "start": start,
            "end": end
        })

        job_available[job_id] = end
        resource_available[machine] = end

        next_operation[job_id] += 1

    return schedule
