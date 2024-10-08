import gradio as gr
from core.simulation import *
from core.resources import *

saved_text = "Moromoro!"
workstation_state = gr.State({ "x": 0, "y": 0})


with open("gui/sim_environment.js", "r") as js_script:
     js_code = "<script>" + js_script.read() + "</script>"
     #js_code = js_script.read()

with open("gui/main.html", "r") as html_page:
     html_code = html_page.read()

with open("gui/gradio_script.js", "r") as gradio_script:
     gr_script = gradio_script.read()

with open("gui/save_btn.js", "r") as save_btn_script:
     process_save_btn_script = save_btn_script.read()


def greet(name, intensity):
    return "Hello, " + name + "!" * int(intensity)


"""

GUI LAYOUT SKETCH:

+-------------------------------------------------------------------------+
|                   Window menu or something                              |
|                   ( Top )                                               |
+-----------------+----------------------------------------+--------------+
|   Tabs?         |                                        |  Tabs?       |
+-----------------+                                        +--------------+
|  Simulation     |       Simulation Environment           |  Tool panel  |
|  control panel  |          ( Center / Right )            |   ( Right )  |
|  ( Left )       |                                        |              |
|                 |                                        |              |
+-----------------+----------------------------------------+--------------+
|                      Simulation Console  ( Bottom )                     |
|                           Input textbox?                                |
+-------------------------------------------------------------------------+


"""


def simulation_environment():
    # Canvas?
    # Tools to create and edit simulation environment. Workstation, worker, material objects... Edit these?
     #sim_script = gr.File("gui/sim_environment.js", visible=False)
     #workstation_list_html = "".join([f'<li draggable="true" data-id="{w["id"]}">{w["name"]}</li>' for w in workstation_dict.workstations]) 
     sim_environment = gr.HTML(html_code)
                      
    # Embed the JavaScript code and HTML structure in a Gradio HTML component
     pass


def simulation_controls():
     # buttons, sliders...
     current_simulation = gr.Dropdown(
                            choices = ["DEMO", "TEST"],
                            label = "Current simulation:",
                            value = "DEMO")
     
     test_textbox = gr.Textbox()
     output_textbox = gr.Textbox()

     save_btn = gr.Button("Save")
     save_btn.click(process_sim_save, [test_textbox], output_textbox, js=process_save_btn_script)


     jobs_btn = gr.Button("Generate job list")
     jobs_btn.click(fn=handle_jobs_button, api_name="jobs")
    
     sim_btn = gr.Button("Simulate")
     sim_btn.click(fn=handle_simulation, api_name="sim")
     
     pass


def simulation_console_output():
     # text box, text input?   
     output = gr.TextArea(label="TODO: simulation results into this box",
                         autoscroll=True,
                         lines=20
                         )
     #input = gr.Textbox(label = "Input textbox option...?")
     pass


def simulation_console_input():
     # text input?
     input = gr.Textbox(label = "Input textbox option...?")
     pass


def handle_simulation():
     run_simulation()


def handle_jobs_button():
     create_jobs(10, [0.66, 1, 1.33])


def update_workstation_location(event_data):
     x = event_data.get("x")
     y = event_data.get("y")
     # ... Placeholder for processing new coordinates
     print(f"Updated workstation location to (X: {x}, Y: {y}).")
     return f"Workstation moved to ({x}, {y})"

def process_sim_save(test_text):
     print(test_text)
     return test_text


def process_workstation_data(data):
    print("process_workstation_data toimii...!")
    print("Data:")
    print(data)
    # ... process the data received from JavaScript
    pass


with gr.Blocks(head=js_code, js=gr_script) as demo:
     with gr.Row():
          with gr.Column(scale = 1):
               simulation_controls()
          with gr.Column(scale = 5, variant="panel"):
               simulation_environment()
     with gr.Row():
         simulation_console_output()
     with gr.Row():
         simulation_console_input()
         output_textbox = gr.Textbox(visible=True)
     output_textbox.change(update_workstation_location, inputs=output_textbox, outputs=None)
     #gr.on(triggers=gr.Trigger("workstation_moved"), fn=update_workstation_location, outputs=[output_textbox])
     #demo.load(None, inputs=None, outputs=None, js="""""")

app = demo.launch()

#app.on("workstation_moved", update_workstation_location, outputs=[output_textbox, event_data_textbox])  # Include the new textbox
#print("workstation_moved event listener attached")  # Add this line
     

