import gradio as gr
from core.simulation import *

def greet(name, intensity):
    return "Hello, " + name + "!" * int(intensity)

def handle_simulation():
        run_simulation()

def handle_jobs_button():
        create_jobs(10, [0.66, 1, 1.33])

with gr.Blocks() as demo:
       
    jobs_btn = gr.Button("Generate job list")
    jobs_btn.click(fn=handle_jobs_button, api_name="jobs")
    
    sim_btn = gr.Button("Simulate")
    sim_btn.click(fn=handle_simulation, api_name="sim")

    output = gr.Textbox(label="TODO: simulation results into this box")