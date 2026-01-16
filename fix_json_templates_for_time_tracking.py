import sys
import json

def modify_tasks_for_time_tracking(task_data):
    """Recursive"""
    for i, step in enumerate(task_data["steps"]):
        if "eta" in step and step["eta"]: del step["eta"]
        if "start" in step and step["start"]: del step["start"]
        if "end" in step and step["end"]: del step ["end"]

        if "steps" in step and step["steps"]:
            if "status" in step and step["status"]: del step["status"]
            if "time_tracking" in step and step["time_tracking"]: del step["time_tracking"]
            modify_tasks_for_time_tracking(step)
        elif "steps" not in step:
            step['status'] = 'pending'
            step["time_tracking"] = {"start_end":[]}


if len(sys.argv) == 2:
    is_single = False
    json_file_path = str(sys.argv[1])
    json_file = None
    with open(json_file_path, 'r') as f:
        json_file = json.load(f)
        if isinstance(json_file, list):
            json_file = json_file[0]
            is_single = True
            modify_tasks_for_time_tracking(json_file)
        else:
            for key, value in json_file.items():
                modify_tasks_for_time_tracking(value)
    with open(json_file_path, 'w') as f:
        if is_single: json_file = [json_file]
        json.dump(json_file, f, indent=4)
else: 
    print("""
          Expected 1 extra argument.
          Example: fix_json_templates_for_time_tracking.py file.json
            """)