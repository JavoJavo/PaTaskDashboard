from nicegui import ui
import json
from typing import List, Optional
import uuid
import yaml
#import watchfiles or watchdog

# Add to your app startup (before UI creation)
ui.add_head_html('''
<style>
  body * {
    -webkit-user-select: text !important;
    -moz-user-select: text !important;
    -ms-user-select: text !important;
    user-select: text !important;
  }
</style>
''')
ui.add_css('''
    /* Make the actual checkbox square smaller */
    .small-checkbox .q-checkbox__bg {
        width: 14px !important;
        height: 14px !important;
        left: 0 !important;
        top: 1px !important;
    }
    
    /* Make the check icon smaller */
    .small-checkbox .q-checkbox__svg {
        font-size: 12px !important;
        width: 12px !important;
        height: 12px !important;
    }
    
    /* Adjust container */
    .small-checkbox .q-checkbox__inner {
        min-width: 14px !important;
        width: 14px !important;
        height: 14px !important;
    }
    
    /* Adjust label position */
    .small-checkbox .q-checkbox__label {
        padding-left: 6px !important;
        font-size: 12px !important;
    }
''')

class BlinkingAlert:
    def __init__(self, message):
        self.message = message
        self.is_red = False
        self.label = ui.label(message).classes('p-4 text-lg transition-colors duration-500')
        
        # Create a timer that toggles the color every 500ms
        self.timer = ui.timer(0.5, self.toggle_color, active=True)
    
    def toggle_color(self):
        self.is_red = not self.is_red
        if self.is_red:
            self.label.classes(replace='bg-red-500 text-white p-4 text-lg transition-colors duration-500')
        else:
            self.label.classes(replace='bg-white text-black p-4 text-lg transition-colors duration-500')
    
    def stop(self):
        self.timer.deactivate()
        self.label.classes(replace='bg-white p-4 text-lg')

# Usage
#alert = BlinkingAlert('WARNING: High CPU usage detected!')

# Left drawer (collapsible side menu)
with open('example_list_of_tasks.yaml', 'r', encoding='utf-8') as file:
    tasks_names_list = yaml.safe_load(file)
current_tasks_names_list = {}
for task in tasks_names_list:
    current_tasks_names_list[task] = False

with ui.left_drawer(value=False).classes('bg-blue-100') as left_drawer:
    #ui.label("LEFT MENU")
    with ui.expansion('Add tasks', icon='add').classes('w-full'):
        with ui.column().classes('gap-0 small-checkbox'):
            checkbox = ui.checkbox('check me').props('dense').classes('text-xs py-0')
            checkbox = ui.checkbox('check me').props('dense').classes('text-xs py-0')
            checkbox = ui.checkbox('check me').props('dense')
            checkbox = ui.checkbox('check me').props('dense')
            for key, value in current_tasks_names_list.items():
                checkbox = ui.checkbox(key,value=value)

# Right drawer (collapsible side menu)
right_drawer = None
with ui.right_drawer().classes('bg-green-100') as right_drawer:
    ui.label("RIGHT MENU")
    ui.button("Close Right", on_click=right_drawer.toggle)


ALL_TASKS = []
FILE = 'Processes.json'
task_in_view = None
# Load sample data
def load_tasks(FILE):
    global ALL_TASKS
    with open(FILE,'r') as f:
        ALL_TASKS = json.load(f)

def save_tasks(FILE, ALL_TASKS):
    with open(FILE, 'w') as f:
        json.dump(ALL_TASKS, f, indent=2)  # indent for readability

try:
    from custom_functions import load_tasks, save_tasks
    ALL_TASKS = load_tasks(FILE)
except:
    load_tasks(FILE)

def code_block(content: str):
    with ui.column().classes('w-full'):
        with ui.row().classes('relative items-center gap-2 p-0 bg-gray-100 dark:bg-gray-800 rounded'):
            ui.markdown(f'```python\n{content}\n```').classes('flex-grow')
            
            # Visible copy button (right side)
            ui.button(icon='content_copy', color='primary') \
                .props('round dense') \
                .classes('shadow') \
                .on('click', lambda: ui.run_javascript(f'navigator.clipboard.writeText(`{content}`)'))
        
def link_block(url: str, display_text: str = None):
    with ui.column().classes('w-full'):
        """Create a copyable link block with icon"""
        display = display_text or url  # Use URL if no display text provided
        with ui.row().classes('items-center w-full bg-gray-100 dark:bg-gray-800 rounded p-2'):
            ui.icon('link').classes('text-blue-500')
            ui.label(display).classes('flex-grow text-sm truncate')
            
            # Compact copy button
            ui.button(icon='content_copy', on_click=lambda: ui.run_javascript(f'navigator.clipboard.writeText(`{url}`)')) \
                .props('flat dense') \
                .classes('w-6 h-6 min-w-0 min-h-0 p-0 m-0 opacity-70 hover:opacity-100')
        
def hint_block(content: str):
    #with ui.expansion('Expand!', caption='Expansion Caption').classes('w-full'):
        #ui.label('inside the expansion')
    pass

tasks_status = {}
def recursive_step_completion_checker(step, completed='completed'):
    if 'steps' in step and step['steps']:
        return all([recursive_step_completion_checker(sub_step,completed=completed) for sub_step in step['steps']])
    else:
        if 'status' not in step: step['status'] = 'pending'
        return (step['status'] == completed)
def update_tasks_status():
    for task in ALL_TASKS:
        task_id = str(task['env'])+'-'+str(task['app'])
        current_tasks_status = 'Not Started'
        for i,step in enumerate(task['steps']):
            if i==0 and recursive_step_completion_checker(step, completed='pending'):
                break
            elif recursive_step_completion_checker(step) == False:
                current_tasks_status = step['name']
                break
            else:
                current_tasks_status = 'Completed'
        tasks_status[task_id] = current_tasks_status
    #print(tasks_status)


def on_changed_checkbox(step):
    if step['status'] == 'completed':
        step['status'] = 'pending'
    else:
        step['status'] = 'completed'
    save_tasks(FILE, ALL_TASKS)
    update_tasks_status()
    draw_drawer_buttons(right_drawer)

def display_task_with_checkboxes(task_data, indent_level=0, is_top_level=True):
    """Recursive checkbox display with proper spacing"""
    with ui.column().classes('w-full gap-0'):  
        for i, step in enumerate(task_data['steps']):            
            with ui.row().classes(f'items-center ml-{indent_level * 4}  p-0 m-0 h-6 hover:bg-gray-100 dark:hover:bg-gray-700'):
                if 'steps' in step and step['steps']:
                    ui.label(f"📌 {step['name']}").classes('text-sm md:text-base font-bold p-1 leading-tight text-primary bg-white/10 rounded')
                else:
                    #print((step['status']=='completed'))
                    if 'status' not in step: step['status'] = 'pending'
                    ui.checkbox(value=(step['status']=='completed'), on_change=lambda s=step: on_changed_checkbox(s)).classes('m-0 p-0 w-3.5 h-3.5 scale-75')
                    ui.label(step['name']).classes('text-xs p-0 leading-none')
            
            with ui.row().classes(f'items-center ml-{indent_level * 4}'):
                if 'content' in step.keys():
                    for [block_type,value] in step['content']:
                        if block_type == 'notes':
                            ui.column().classes('w-full')
                            with ui.row().classes('w-full ml-8'):
                                ui.markdown(value).classes('ml-8 text-xs p-0 leading-none')
                        elif block_type == 'command_block':
                            code_block(value)
                        elif block_type == 'link_block':
                            link_block(value)
                        
                    #ui.markdown('''This is **Markdown**  
                    #            sdfgasdf''').classes('ml-8 text-xs p-0 leading-none')
                
            # Recursive call with +1 level (not +2)
            if 'steps' in step and step['steps']:
                display_task_with_checkboxes(step, indent_level + 2, False)  # Fixed from +2 to +1

#task_scroll_positions = {}
def main_section(task, i=None):
    current_task = ALL_TASKS.pop(i)
    ALL_TASKS.insert(0, current_task)
    draw_drawer_buttons(right_drawer)
    main_section_ui.clear()
    task_key = f"{task['env']}-{task['app']}"
    task_in_view = task_key
    with main_section_ui:
        ui.label(f"🏭 {task['app']} - {task['env']}").classes('sticky top-0 z-10 text-lg md:text-xl font-bold p-2 mb-4 bg-blue-50 dark:bg-blue-900/30 text-blue-800 dark:text-blue-200 rounded-lg border-l-4 border-blue-500 w-full shadow-sm')
        
        # Create a unique scroll container for each task
        #with ui.card().classes('w-full'):
        #    ui.scroll_area(on_scroll=lambda e: print(e.vertical_percentage))
            

        display_task_with_checkboxes(task, 0, False)
update_tasks_status()

def load_status_config(filepath='example_status_config.json'):
    """Load status configuration from JSON file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)
    except:
        print("Could not load file: status_config.json")
        return None
    
    
def draw_drawer_buttons(right_drawer):
    right_drawer.clear()
    
    # Status definitions with card colors and subtle gradients
    status_config = load_status_config()

    for i,task in enumerate(ALL_TASKS):
        task_key = f"{task['env']}-{task['app']}"
        status = tasks_status.get(task_key, "Unknown")
        config = status_config.get(status, {
            "icon": "❓",
            "color": "bg-grey-50",
            "border": "border-l-grey-500",
            "progress": 0.0
        })
        base_color = task.get("border", "").replace("border-l-", "")  # e.g. "red-500"
        highlight = (
            f"ring-8 ring-{base_color} border-l-8 shadow-2xl "#animate-pulse "
            f"bg-gradient-to-r from-{base_color.replace('-500','-50')} "
            f"to-{base_color.replace('-500','-100')} "
            f"dark:from-{base_color.replace('-500','-900')} "
            f"dark:to-{base_color.replace('-500','-800')}"
            if i == 0 else ""
        )
        with right_drawer:
            with ui.card().classes(f"""
                w-full mb-1 p-0 overflow-hidden
                {config['color']} {config['border']}
                border-l-4 rounded-lg shadow-sm
                hover:shadow-md transition-shadow
                cursor-pointer
                flex-none
                {highlight}
                """).on("click", lambda t=task, idx=i: main_section(t,i=idx)):
                
                # Tight header with original sizes
                with ui.row().classes("w-full px-2 pt-1 items-center justify-between"):
                    ui.label(f"🏭 {task['app']} - {task['env']}").classes("font-bold")
                    ui.label(config['icon']).classes("text-xl")
                
                # Progress bar moved up with no margin
                ui.linear_progress(config['progress'], show_value=False).classes("h-1.5 w-full mt-0")
                
                # Compact footer with original text size
                with ui.row().classes("w-full px-2 pb-1 items-center justify-between"):
                    ui.label(status).classes("font-medium")
                    ui.icon("chevron_right").classes("text-gray-500")
                    

# Minimalist layout with better spacing
with ui.column().classes('w-full h-full p-2 gap-2 relative'):  # ← Add 'relative' container
    # Header with integrated controls (no overlap)
    with ui.row().classes('w-full justify-between items-center p-1 mb-2 sticky top-0 z-10 bg-white dark:bg-gray-900'):
        ui.label('').classes('flex-grow')  # Spacer
        with ui.row().classes('gap-1'):
            ui.button(icon='menu', on_click=left_drawer.toggle).props('flat dense')
            ui.button(icon='settings', on_click=right_drawer.toggle).props('flat dense')
    
    main_section_ui = ui.column().classes('w-full') 
    draw_drawer_buttons(right_drawer)
    main_section(ALL_TASKS[0], i=0)        # Right drawer:
        #with right_drawer:
            #draw_drawer_buttons(right_drawer)
            #ui.button(f"🏭 {task['app']} - {task['env']}\n{tasks_status[str(task['env'])+'-'+str(task['app'])]}", on_click=lambda t=task: main_section(t))

ui.dark_mode().enable
ui.run(native=True)