// Canvas setup

console.log("Jotain jotain...");

let canvas = document.getElementById("simulationCanvas");
let ctx = canvas.getContext("2d");


// Workstation list (replace with your actual data)
//const workstationList = document.getElementById('workstationList');
let workstations = [
    { id: 1, name: "Workstation 1", x: 0, y: 0 }
    // ... more workstations
];


// Drawing functions (replace with your actual visualization logic)
function drawWorkstation(workstation) {
    ctx.fillStyle = "blue";
    ctx.fillRect(workstation.x, workstation.y, workstation.x + 50, workstation.y + 30);
    ctx.fillStyle = "white";
    ctx.fillText(workstation.name, workstation.x + 10, workstation.y + 20);
}


// Initial drawing (if needed)
function initializeCanvas() {
    console.log("Jotain jotain...");
    if (workstations.length > 0) {
        drawWorkstation(workstations[0]);
    }

}
function wrap() {
    function test() {
        document.getElementById('demo').innerHTML = "Hello"
    }
}


function createGradioAnimation() {
    var container = document.createElement('div');
    container.id = 'gradio-animation';
    container.style.fontSize = '2em';
    container.style.fontWeight = 'bold';
    container.style.textAlign = 'center';
    container.style.marginBottom = '20px';

    var text = 'Welcome to Gradio!';
    for (var i = 0; i < text.length; i++) {
        (function(i){
            setTimeout(function(){
                var letter = document.createElement('span');
                letter.style.opacity = '0';
                letter.style.transition = 'opacity 0.5s';
                letter.innerText = text[i];

                container.appendChild(letter);

                setTimeout(function() {
                    letter.style.opacity = '1';
                }, 50);
            }, i * 250);
        })(i);
    }

    var gradioContainer = document.querySelector('.gradio-container');
    gradioContainer.insertBefore(container, gradioContainer.firstChild);

    return 'Animation created';
}

document.addEventListener("DOMContentLoaded", (event) => {
    setTimeout(100);
    console.log("Jotain jotain...");
    confirm("createWorkstation!");
    createGradioAnimation();
    initializeCanvas();
});


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