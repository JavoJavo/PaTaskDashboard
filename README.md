# Example Tasks displayed at PaTaskDashboard UI
Build with niceGUI.     
Developed to keep track of different processes taking place at the same time. 
<img width="1364" height="719" alt="image" src="https://github.com/user-attachments/assets/0bf7c1ad-6ac7-4bf1-bf35-5254edd25c2c" />
## TODO
- Time tracking
    - Logic:
        - Time delta between checking checkboxes will be recorded.
        - When first checkbox is checked, start first start and end time for first end will be the same and time will be recorded. (Maybe add start checkbox at the begining of every process.)
        - When second, third, ..., n, checkbox is checked,  end time of last checked checkbox will be start time of n checkbox that was checked, end time will be time when the box was checked.
        - If checkbox is unchecked, same logic will be followed, so it is possible that one single step has multiple tuples of time which will be summed to calculate total execution time.
        - There are obviously errors (mostly if user doesn't stick to the method and plays with checkboxes) but I think it's a good start.
        - Data structures:
            - Global variable that will save last end time, it can be written to json.
            - Variables per-step that will record start and end times in a list of tuples (start, end)
            - More variables for future development like opt-out toggle 
    - Exceptions:
        - Waiting: there has to be a way to record waiting time. Maybe a pause/play button that funtions exactly like another checkbox but with different UI design.
        - Opt in or out (with button or something in the UI) of registering or taking time spent "seriously" for particular task. Why?:
            - Parallel tasks: some tasks may be done at the same time, but current system only tracks (for now) one task at a time.
            - Forgetting to check tasks or registering pauses.
        - UI for manually editing time for specific tasks (without corrupting end-time variable)
        - Add undo button. For when accidentally checking a box that one was not working on by mistake, maybe confused processes, boxes, etc.
- Data saved in different format than just a copy of json, maybe ID everything and just save (ID, value) tuples. Build loaders and savers for that format.
- Error tracking. Inputing error reason, screenshot, etc.
- Skipping tracking.
- WA enabling and tracking after expected errors.
- Analytics, data visualizations with data generated
- Anomaly detections, alarms (for example when process is taking long time)
- Track running tasks some way (other than delta between checkboxes clicks). Maybe implament start/pause/finish/failed/etc button within single tasks.
- Make new page for process viewing, editing and creation
