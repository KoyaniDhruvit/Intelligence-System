
# FIFO Scheduling Algorithm

def fifo_scheduling(jobs, resources):

    # Get machine IDs from operations
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

        job = ready_jobs[0]
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
