import sys, os
import json, yaml
from pathlib import Path

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
            step["status"] = "pending"
            step["time_tracking"] = {"start_end":[]}


    
def get_PATH():
    #EXE_DIR = os.path.dirname(sys.executable)
    #PATH = os.path.join(EXE_DIR, path)
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)+'/'
    return os.path.dirname(os.path.abspath(__file__))+'/'

def load_file_path_conf():
    with open(get_PATH()+'file_path_conf.yaml', 'r') as f:
        config = yaml.safe_load(f)
        return config
config = load_file_path_conf()



single_file_processes_dir = get_PATH() + config["paths"]["input"]["single_file_processes_dir"]
json_file = None

for filename in os.listdir(single_file_processes_dir):
    filepath = os.path.join(single_file_processes_dir, filename)
    # Check if the path points to a file (and not a directory)
    if os.path.isfile(filepath):
        print("Updating "+filepath)
        with open(filepath, "r") as f:
            json_file = json.load(f)
            json_file = json_file[0]
            json_file["global_time_pointer"] = "None"
            modify_tasks_for_time_tracking(json_file)
        with open(filepath, "w") as f:
            json_file = [json_file]
            json.dump(json_file, f, indent=4)
        print("Updating "+filepath+" COMPLETED.")


template_file = get_PATH() + config["paths"]["input"]["tasks_template"]
json_file = None

print("Updating "+template_file)
with open(template_file, "r") as f:
    json_file = json.load(f)
    for key, value in json_file.items():
        json_file[key]["global_time_pointer"] = "None"
        modify_tasks_for_time_tracking(value)
with open(template_file, "w") as f:
    json.dump(json_file, f, indent=4)
print("Updating "+template_file+" COMPLETED.")


'''

is_single = False
json_file = None
if len(sys.argv) == 2:
    is_single = False
    json_file_path = str(sys.argv[1])
    json_file = None
    with open(json_file_path, "r") as f:
        json_file = json.load(f)
        if isinstance(json_file, list):
            json_file = json_file[0]
            is_single = True
            json_file["global_time_pointer"] = "None"
            modify_tasks_for_time_tracking(json_file)
        else:
            for key, value in json_file.items():
                json_file[key]["global_time_pointer"] = "None"
                modify_tasks_for_time_tracking(value)
    with open(json_file_path, "w") as f:
        if is_single: json_file = [json_file]
        json.dump(json_file, f, indent=4)
else: 
    print("""
          Expected 1 extra argument.
          Example: fix_json_templates_for_time_tracking.py file.json
            """)
'''