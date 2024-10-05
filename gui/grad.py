import gradio as gr
from core.simulation import *
from core.resources import *

with open("gui/sim_environment.js", "r") as js_script:
     js_code = "<script>" + js_script.read() + "</script>"
     #js_code = js_script.read()

with open("gui/main.html", "r") as html_page:
     html_code = html_page.read()

with open("gui/gradio_script.js", "r") as gradio_script:
     gr_script = gradio_script.read()


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


"""
                                <script>

                                let canvas = document.getElementById('simulationCanvas');
                                let ctx = canvas.getContext('2d');

                                let blocks = [
                                    {{id: 1, name: 'Block 1', x: 0, y: 0}}
                                ];

                                function drawBlocks(block) {{
                                    ctx.fillStyle = 'blue';
                                    ctx.fillRect(block.x, block.y, 50, 30);
                                    ctx.fillStyle = 'white';
                                    ctx.fillText(block.name, block.x + 10, block.y + 20);
                                }}

                                function initializeCanvas() {{
                                    canvas.style.border = '5px red';
                                    canvas.height = 600;
                                    canvas.width = 400;
                                    if (blocks.length > 0) {{
                                        drawBlocks(blocks[0]);
                                    }}
                                }}

                                //document.addEventListener('DOMContentLoaded', initializeCanvas);

                                initializeCanvas();

                                </script>
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

