// Canvas setup
let canvas = document.getElementById('simulationCanvas');
let ctx = canvas.getContext('2d');


// Workstation list (replace with your actual data)
//const workstationList = document.getElementById('workstationList');
let workstations = [
    { id: 1, name: 'Workstation 1', x: 0, y: 0 }
    // ... more workstations
];
/*
// Drag-and-drop functionality
let draggedWorkstation = null;

workstationList.addEventListener('dragstart', (event) => {
    draggedWorkstation = event.target;
});

canvas.addEventListener('dragover', (event) => {
    event.preventDefault();
});

canvas.addEventListener('drop', (event) => {
    event.preventDefault();
    const rect = canvas.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;  

    // Create a new workstation on the canvas (replace with your actual logic)
    const newWorkstation = { 
        id: draggedWorkstation.dataset.id, 
        name: draggedWorkstation.textContent,
        x,
        y
    };
    drawWorkstation(newWorkstation);

    // ... (Add the new workstation to your simulation data)
});

canvas.addEventListener('onclick', testMsg);

function testMsg() {
    confirm("Toimii!");
    console.log("Toimii!");
};
*/

// Drawing functions (replace with your actual visualization logic)
function drawWorkstation(workstation) {
    ctx.fillStyle = 'blue';
    ctx.fillRect(workstation.x, workstation.y, workstation.x + 50, workstation.y + 30);
    ctx.fillStyle = 'white';
    ctx.fillText(workstation.name, workstation.x + 10, workstation.y + 20);
}

function createWorkstation(){
    confirm("createWorkstation!");
}

// Initial drawing (if needed)
function initializeCanvas() {
    // ... (Draw any initial elements on the canvas)
    canvas.style.border = '5px red';
    //drawWorkstation(workstations.getElementById(1));

    if (workstations.length > 0) {
        drawWorkstation(workstations[0]);
    }

}

//document.addEventListener('DOMContentLoaded', initializeCanvas);

initializeCanvas();