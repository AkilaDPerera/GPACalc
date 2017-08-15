// active page highlight
function setActive(){
	var path = window.location.pathname;
	switch(path){
		case "/":{
			document.getElementById("home").className="active";
			break;
		}
		case "/professional/":{
			document.getElementById("professional").className="active";
			break;
		}
		case "/projects/":{
			document.getElementById("projects").className="active";
			break;
		}
		case "/gpa/auto/":{
			document.getElementById("gpa_auto").className="active";
			break;
		}
		case "/contact/":{
			document.getElementById("contact").className="active";
			break;
		}
		default:{
			document.getElementById("gpa_auto").className="active";
		}
	}
}

// Login info handle
function setLogin(){
	var getUserRQ = $.get( "/get_user/");
	getUserRQ.done(function(data) {
		if(data["user"]=="None"){
			document.getElementById("user").style.display = "None";
			document.getElementById("login").innerHTML="<span class=\"glyphicon glyphicon-log-in\"></span> Login";
		}else{
			document.getElementById("user").innerHTML="<span class=\"glyphicon glyphicon-user\"></span> "+data["user"];
			document.getElementById("login").innerHTML="<span class=\"glyphicon glyphicon-log-out\"></span> Log out";
		}
	});
}

location.assign("https://akiladperera.alwaysdata.net/");