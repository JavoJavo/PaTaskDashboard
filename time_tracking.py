import time

def now():
    return time.time()

def register_time(step_tracking, global_time_pointer):
    end_time = now()
    start_time = global_time_pointer
    if start_time == "None":
        start_time = end_time
    step_tracking["start_end"].append((start_time, end_time))
    global_time_pointer = end_time
    return global_time_pointer

# Not necessary, register_time handles it:
#def register_time_when_unchecked(step_tracking, global_time_pointer):
#    end_time = now(