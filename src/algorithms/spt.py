
# SPT Scheduling Algorithm

def spt_scheduling(jobs, resources):

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

        ready_operations = []

        for job in jobs:
            job_id = job["id"]

            if next_operation[job_id] < len(job["operations"]):

                operation_index = next_operation[job_id]
                operation = job["operations"][operation_index]

                machine = operation["resource"]

                ready_time = max(
                    job_available[job_id],
                    resource_available[machine]
                )

                ready_operations.append({
                    "job": job,
                    "job_id": job_id,
                    "operation_index": operation_index,
                    "operation": operation,
                    "machine": machine,
                    "ready_time": ready_time
                })

        selected = min(
            ready_operations,
            key=lambda item: (
                item["operation"]["duration"],
                item["job_id"]
            )
        )

        job_id = selected["job_id"]
        operation_index = selected["operation_index"]
        operation = selected["operation"]
        machine = selected["machine"]

        start = selected["ready_time"]
        end = start + operation["duration"]

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
