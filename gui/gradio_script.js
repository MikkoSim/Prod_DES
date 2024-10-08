/*


  ALL CODE MUST BE WITHIN A WRAPPER FUNCTION. IN THIS CASE, TEST1 !!!
  GRADIO EXECUTES CODE WITHIN A WRAPPER FUNCTION. ANYTHING OUTSIDE WILL
  LEAD TO SYNTAX ERROR ETC.


*/

function test1() {
    // setTimeout(() => { }, 100);  // Introduce a slight delay

    canvas = document.getElementById("simulationCanvas");
    //canvas.addEventListener('onclick', testMsg);
    ctx = canvas.getContext("2d");


    initializeCanvas();


    canvas.onmousedown = mouse_down;
    canvas.onmouseup = mouse_up;
    canvas.onmouseout = mouse_out;
    canvas.onmousemove = mouse_move;

    

}