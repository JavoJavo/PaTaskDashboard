from nicegui import ui
import json
from typing import List, Optional
import uuid

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
with ui.left_drawer(value=False).classes('bg-blue-100') as left_drawer:
    ui.label("LEFT MENU")
    ui.button("Option 1")
    ui.button("Option 2")
    ui.button("Close Left", on_click=left_drawer.toggle)

# Right drawer (collapsible side menu)
with ui.right_drawer().classes('bg-green-100') as right_drawer:
    ui.label("RIGHT MENU")
    ui.button("Setting A")
    ui.button("Setting B")
    ui.button("Close Right", on_click=right_drawer.toggle)


ALL_TASKS = []

# Load sample data
def load_tasks():
    global ALL_TASKS
    with open('Processes.json','r') as f:
        ALL_TASKS = json.load(f)
load_tasks()

def code_block(content: str):
    with ui.row().classes('relative items-center gap-2 p-0 bg-gray-100 dark:bg-gray-800 rounded'):
        ui.markdown(f'```python\n{content}\n```').classes('flex-grow')
        
        # Visible copy button (right side)
        ui.button(icon='content_copy', color='primary') \
            .props('round dense') \
            .classes('shadow') \
            .on('click', lambda: ui.run_javascript(f'navigator.clipboard.writeText(`{content}`)'))
        
def link_block(url: str, display_text: str = None):
    """Create a copyable link block with icon"""
    display = display_text or url  # Use URL if no display text provided
    with ui.row().classes('items-center w-full bg-gray-100 dark:bg-gray-800 rounded p-2'):
        ui.icon('link').classes('text-blue-500')
        ui.label(display).classes('flex-grow text-sm truncate')
        
        # Compact copy button
        ui.button(icon='content_copy', on_click=lambda: ui.run_javascript(f'navigator.clipboard.writeText(`{url}`)')) \
            .props('flat dense') \
            .classes('w-6 h-6 min-w-0 min-h-0 p-0 m-0 opacity-70 hover:opacity-100')
        
def display_task_with_checkboxes(task_data, indent_level=0, is_top_level=True):
    """Recursive checkbox display with proper spacing"""
    with ui.column().classes('w-full gap-0'):  
        for i, step in enumerate(task_data['steps']):            
            with ui.row().classes(f'items-center ml-{indent_level * 4}  p-0 m-0 h-6 hover:bg-gray-100 dark:hover:bg-gray-700'):
                if 'steps' in step and step['steps']:
                    ui.label(f"📌 {step['name']}").classes('text-sm md:text-base font-bold p-1 leading-tight text-primary bg-white/10 rounded')
                else:
                    ui.checkbox().classes('m-0 p-0 w-3.5 h-3.5 scale-75')
                    ui.label(step['name']).classes('text-xs p-0 leading-none')
            
            with ui.row().classes(f'items-center ml-{indent_level * 4}'):
                if 'content' in step.keys():
                    for [block_type,value] in step['content']:
                        if block_type == 'notes':
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


# Minimalist layout with better spacing
with ui.column().classes('w-full h-full p-2 gap-2 relative'):  # ← Add 'relative' container
    # Header with integrated controls (no overlap)
    with ui.row().classes('w-full justify-between items-center p-1 mb-2 sticky top-0 z-10 bg-white dark:bg-gray-900'):
        ui.label('').classes('flex-grow')  # Spacer
        with ui.row().classes('gap-1'):
            ui.button(icon='menu', on_click=left_drawer.toggle).props('flat dense')
            ui.button(icon='settings', on_click=right_drawer.toggle).props('flat dense')
     
    for task in ALL_TASKS:
        with ui.card().classes('w-full p-0 m-0 gap-0'):
            ui.label(f"🏭 {task['app']} - {task['env']}").classes('text-lg md:text-xl font-bold p-2 mb-4 bg-blue-50 dark:bg-blue-900/30 text-blue-800 dark:text-blue-200 rounded-lg border-l-4 border-blue-500 w-full shadow-sm')
            with ui.scroll_area().classes('w-full h-[700px] dense-scroll-area p-0'):
                display_task_with_checkboxes(task, 0, False)


with ui.scroll_area().classes('w-300 h-50 border'):
    with ui.stepper().props('vertical').classes('w-full') as stepper:
        with ui.step('Preheat'):
            ui.label('Preheat the oven to 350 degrees')
            with ui.stepper_navigation():
                ui.button('Next', on_click=stepper.next)
        with ui.step('Ingredients'):
            ui.label('Mix the ingredients')
            with ui.stepper_navigation():
                ui.button('Next', on_click=stepper.next)
                ui.button('Back', on_click=stepper.previous).props('flat')
        with ui.step('Bake'):
            ui.label('Bake for 20 minutes')
            with ui.stepper_navigation():
                ui.button('Done', on_click=lambda: ui.notify('Yay!', type='positive'))
                ui.button('Back', on_click=stepper.previous).props('flat')



    # Create an element that blinks
    #with ui.row():
    #    ui.button('Stop Alert', on_click=alert.stop)
    #    ui.button('New Alert', on_click=lambda: BlinkingAlert('NEW ALERT!'))

ui.dark_mode().enable
ui.run(native=True)