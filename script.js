document.addEventListener('DOMContentLoaded', function() {
  let joystickIsVisible = false;
  let joystickContainer = document.getElementById("joystick-container");
  let joystick = document.getElementById("joystick");
  let orig;
  
  let onMouseDown = function(e) {
    if (joystickIsVisible) return;
    
    orig = {x: e.changedTouches[0].pageX, y: e.changedTouches[0].pageY};
    
    joystickContainer.classList.add("visible");
    joystickContainer.style.left = orig.x + "px";
    joystickContainer.style.top = orig.y + "px";
    
    joystick.style.left = "100px";
    joystick.style.top = "100px";
    
    joystickIsVisible = true;
  }
  
  let onMouseMove = function(e) {
    if (!joystickIsVisible) return;
    
    let x = e.changedTouches[0].pageX - orig.x;
    let y = e.changedTouches[0].pageY - orig.y;
    let d = Math.sqrt(x * x + y * y);
    if (d > 100) {
      x *= 100 / d;
      y *= 100 / d;
    }
    x += 100;
    y += 100;
    
    joystick.style.left = x + "px";
    joystick.style.top = y + "px";

    // Normalize coordinates
    x = (x - 100) / 100;
    y = (y - 100) / 100;
		socket.send(x + "," + y);
  }
  
  let onMouseUp = function() {
    joystickContainer.classList.remove("visible");
    joystickIsVisible = false;
    socket.send("0,0");
  }
  
  document.addEventListener('touchstart', onMouseDown);
  document.addEventListener('touchmove', onMouseMove);
  document.addEventListener('touchend', onMouseUp);

	let socket = null;
	try {
		socket = new WebSocket("ws://192.168.0.22:8765");
	} catch (exception) {
		console.error(exception);
    return;
	}

	socket.onerror = function(error) {
		console.error(error);
	};

	socket.onopen = function(event) {
		console.log("Connexion établie.");

		this.onclose = function(event) {
			console.log("Connexion terminée.");
		};

		this.onmessage = function(event) {
			console.log("Message:", event.data);
		};
	};

});

