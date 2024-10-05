
//
//  TEST FUNCTIONS
//

function click_text() {
    alert('JS pätkä toimii!');
    document.getElementById('otsikko').innerHTML = "MUUTTUI!";
}


function inc_num() {
    num = num + 1;
    document.getElementById('numero').innerHTML = num;
}


function getRandomInt(max) {
    return Math.floor(Math.random() * max);
}


function rnd_num() {
    num = getRandomInt(100);
    document.getElementById('numero').innerHTML = num;
}



// Drawing functions (replace with your actual visualization logic)
function drawWorkstation(workstation) {
    ctx.fillStyle = "blue";
    ctx.fillRect(workstation.x, workstation.y, workstation.x + 80, workstation.y + 30);
    ctx.fillStyle = "white";
    ctx.fillText(workstation.name, workstation.x + 10, workstation.y + 20);
    console.log("Drew workstation at: (X: ", workstation.x, ", Y: ", workstation.y, ")");
}

function clearCanvas() {
    ctx.clearRect(0,0, 600, 400);
}


// Initialize canvas. Update draw all objects from back-end.
function initializeCanvas() {
    console.log("initializeCanvas...");
    if (workstations.length > 0) {
        drawWorkstation(workstations[0]);
    }
}


function updateCanvas() {
    // Set some time interval, trigger etc. to update canvas events.
    // Show animation of changes at events.
    clearCanvas();
    for (let workstation of workstations) {
        drawWorkstation(workstation);
    }
}





//let canvas = document.getElementById("simulationCanvas");
let canvas = null;
let ctx = null;
let draggedWorkstation = null;

let num = 0;

let workstations = [ ];
let current_workstation_index = null;

workstations.push( { id: 0, name: "Workstation 1", x: 0, y: 0 } );

let is_dragging = false;
let startX = null, startY = null;

let is_mouse_on_workstation = function(x, y, workstation) {
    let workstation_left = workstation.x;
    let workstation_right = workstation.x + 80;
    let workstation_top = workstation.y;
    let workstation_bottom = workstation.y + 30;

    if(x > workstation_left && x < workstation_right && y > workstation_top && y < workstation_bottom) {
        return true;
    }

    return false;
}


let mouse_down = function(event) {
    event.preventDefault();
    
    startX = parseInt(event.offsetX);
    startY = parseInt(event.offsetY);

    let index = 0;

    for (let workstation of workstations) {
        if(is_mouse_on_workstation(startX, startY, workstation)) {
            console.log("Mouse is on workstation!")
            current_workstation_index = index;
            is_dragging = true;
            console.log("Dragging workstation: ", current_workstation_index);
            return;
        }

        index++;
    }

}


let mouse_up = function(event) {
    if (!is_dragging) {
        return;
    }
    event.preventDefault();
    is_dragging = false;
}


let mouse_out = function(event) {
    if (!is_dragging) {
        return;
    }
    event.preventDefault();
    is_dragging = false;
}

let mouse_move = function(event) {
    if(!is_dragging) {
        return;
    }


    if (is_dragging) {
        event.preventDefault();
        let mouseX = parseInt(event.offsetX);
        let mouseY = parseInt(event.offsetY);

        let dx = mouseX - startX;
        let dy = mouseY - startY;

        workstations[current_workstation_index].x += dx;
        workstations[current_workstation_index].y += dy;

        console.log("Workstation moved from: (X: ", startX, ", Y: ", startY, ")");
        console.log("To: (X: ", mouseX, ", Y: ", mouseY, ")");

        updateCanvas();

        startX = mouseX;
        startY = mouseY;

    }
}


/*

// Drag-and-drop functionality

test_workstation.addEventListener('dragstart', (event) => {
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

*/



