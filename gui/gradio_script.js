/*


  ALL CODE MUST BE WITHIN A WRAPPER FUNCTION. IN THIS CASE, TEST1 !!!
  GRADIO EXECUTES CODE WITHIN A WRAPPER FUNCTION. ANYTHING OUTSIDE WILL
  LEAD TO SYNTAX ERROR ETC.


*/

function test1() {
    // setTimeout(() => { }, 100);  // Introduce a slight delay

    console.log("DOMContentLoaded...");
    canvas = document.getElementById("simulationCanvas");
    ctx = canvas.getContext("2d");

    initializeCanvas();

}