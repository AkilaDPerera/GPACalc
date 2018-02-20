function SGPA(element, SGPATempLoc){
	var map = {'A+':4.2, 'A':4.0, 'A-':3.7, 'B+':3.3, 'B':3.0, 'B-':2.7, 'C+':2.3, 'C':2.0, 'C-':1.5, 'D':1.0, 'F':0.0};
	var trs = element.parentElement.parentElement.parentElement.getElementsByTagName("tr");
	var credit;
	var grade;
	
	var totCredits = 0;
	var sumOfCreditXgrade = 0;
	for(var i=0; i<trs.length; i++){
		credit = parseFloat(trs[i].getElementsByTagName("td")[2].innerHTML);
		grade = trs[i].getElementsByTagName("select")[0].value
		if(grade!="UNKNOWN" && grade!="Non-GPA"){
			totCredits += credit;
			sumOfCreditXgrade += map[grade]*credit;
		}
	}
	if(totCredits!=0){
		document.getElementById(SGPATempLoc).innerHTML = (sumOfCreditXgrade/totCredits).toFixed(2);;
	}else{
		document.getElementById(SGPATempLoc).innerHTML = "0.00";
	}
}

function setImage(className){
	if("----"==className){
		document.getElementById("imgComp").style.display = "None";
	}
}

function submit(parent){
	parent.innerHTML = "<span class=\"fa fa-refresh fa-spin\" style=\"font-size:24px\"></span>";
	parent.disabled = true;
	
	var data = parent.parentElement.parentElement.getElementsByTagName("select");
	var token = document.getElementById("token");
	var dataDic = {};

	dataDic[token.name]=token.value;
	for(var i=0; i<data.length; i++){
		dataDic[data[i].name]=data[i].value;
	}
	
	//send the request
	var request = $.post( "/gpa/auto/submit/", dataDic);
	request.done(function(data) {
		location.assign("/gpa/auto/");
	});
}

function alertAutoHide(){
	divAlert = document.getElementById("alertToJuniors");
	setTimeout(function(){
		divAlert.style.display = "None";
	}, 10000);
}

//review delete by id
function reviewDeleteById(parent){
	var token = document.getElementById("token");
    var dataDic = {
  		  "csrfmiddlewaretoken": token.value,
  		  "id": parent.id
    };
    parent.innerHTML = "<span class=\"fa fa-refresh fa-spin\" style=\"font-size:24px\"></span>";
    
	var rq = $.post( "/gpa/auto/deleteReviews/", dataDic);
    rq.done(function(data) {
    	//format new reviews set
    	var reviewSet = document.getElementById("review-set");
		reviewSet.innerHTML = "";
		for(var i in data){
			review = data[i];
		
			//set profile details string
			var profileDetails = review.user + " - " + review.index + " | <span>";
			for(var s=0; s<review.rate; s++){
				  profileDetails += "<i class=\"fa fa-star\" aria-hidden=\"true\" style=\"color: rgb(247, 183, 62);\"></i>";
			}
			profileDetails += "</span>";
			  
			//set delete btn
			var deleteString = "";
			if(review.isDeleteEnable){
				  deleteString = "<span id=" + review.id + " class=\"pull-right\" style=\"cursor: pointer;\"><a onClick=\"reviewDeleteById(this.parentElement);\">delete</a></span>"
			}
			  
			var msg = "</div><div>" + review.message + "</div></div>";
			  
			var inner = "<div class=\"panel-body\"><div>" + profileDetails + deleteString + msg;
			  
			reviewSet.innerHTML += inner;
		}
    });
}

//Accept feedback
$(document).ready(function() {
	$('#submitFeedback').click(function(event) {
		var isvalidate = $("#ratingsForm")[0].checkValidity();
	    if (isvalidate) {
	      event.preventDefault();

	      var token = document.getElementById("token");
	      var message = document.getElementById("comment");
	      var rate = document.querySelector('input[name="star"]:checked')
	      
	      
	      var dataDic = {
	    		  "csrfmiddlewaretoken": token.value,
	    		  "message": message.value,
	    		  "rate": rate.value
	      };
	      
	      var subBtn = document.getElementById("submitFeedback");
	      subBtn.innerHTML = "<span class=\"fa fa-refresh fa-spin\"></span>";
	      subBtn.disabled = true;
	      
	      var rq = $.post( "/gpa/auto/postFeedback/", dataDic);
	      rq.done(function(data) {
	    	  
	    	  //format new reviews set
	    	  var reviewSet = document.getElementById("review-set");
	    	  reviewSet.innerHTML = "";
	    	  for(var i in data){
	    		  review = data[i];

	    		  //set profile details string
	    		  var profileDetails = review.user + " - " + review.index + " | <span>";
	    		  for(var s=0; s<review.rate; s++){
	    			  profileDetails += "<i class=\"fa fa-star\" aria-hidden=\"true\" style=\"color: rgb(247, 183, 62);\"></i>";
	    		  }
	    		  profileDetails += "</span>";
	    		  
		  		  //set delete btn
		  		  var deleteString = "";
		  		  if(review.isDeleteEnable){
		  			  deleteString = "<span id=" + review.id + " class=\"pull-right\" style=\"cursor: pointer;\"><a onClick=\"reviewDeleteById(this.parentElement);\">delete</a></span>"
		  		  }
		  			  
		  		  var msg = "</div><div>" + review.message + "</div></div>";
	    		  
	    		  var inner = "<div class=\"panel-body\"><div>" + profileDetails + deleteString + msg;
	    		  
	    		  reviewSet.innerHTML += inner;
	    	  }

	    	  //reset data
	    	  document.getElementById("star-5").checked = true;
	    	  document.getElementById("comment").value = "";
	    	  document.getElementById("submitFeedback").innerHTML = "Submit";
	    	  subBtn.disabled = false;
	      });
	    }
	});
});

function getMarkSheetURL(){
	var data = document.getElementsByTagName("select");
	var token = document.getElementById("token");
	
	var dataDic = {};
	modules = [];
	for(var i=0; i<data.length; i++){
		modules.push(data[i].name);
	}
	
	dataDic[token.name] = token.value;
	dataDic['modules'] = modules;

    var rq = $.post( "/gpa/auto/getMarkSheetURLs/", dataDic);
    rq.done(function(data) {
    	for(var i=0; i<data.length; i++){
    		entry = data[i];
    		td = document.getElementById("code"+entry[0]);
    		btns = td.getElementsByTagName("button");
    		
    		//handling non gpa entries
    		if (entry[4]==true){
    			tr = td.parentElement;
    			tr.style.backgroundColor = "rgba(255, 235, 0, 0.15)";
    			tr.setAttribute("title", entry[5]+"% of people indicate this module as non GPA. Please double check before consider this module as GPA.");
    			trModal = document.getElementById("modalModule"+entry[0]);
    			trModal.style.backgroundColor = "rgba(255, 235, 0, 0.15)";
    			trModal.setAttribute("title", entry[5]+"% of people indicate this module as non GPA. Please double check before consider this module as GPA.");
    		}

    		switch (entry[1]){
    		   case "NW": 
    			   btns[1].style.display = "inline-block";
    			   break;
    			   
    		   case "PD": 
    			   btns[2].style.display = "inline-block";
    			   if(entry[2]===true){btns[3].style.display = "inline-block";}
    			   break;
    			   
    		   case "VW": 
    			   btns[0].style.display = "inline-block";
    			   btns[0].getElementsByTagName("a")[0].setAttribute("href", entry[3]);
    		       break;
    		       
    		   case "VWAD": 
    			   btns[0].style.display = "inline-block";
    			   btns[0].getElementsByTagName("a")[0].setAttribute("href", entry[3]);
    			   btns[1].style.display = "inline-block";
    		       break;
    		       
    		   case "VWADPD": 
    			   btns[0].style.display = "inline-block";
    			   btns[0].getElementsByTagName("a")[0].setAttribute("href", entry[3]);
    			   btns[2].style.display = "inline-block";
    			   if(entry[2]===true){btns[3].style.display = "inline-block";}
    		       break;
    		       
    		   default: 
    			   btns[0].style.display = "None";
	    		   btns[1].style.display = "None";
	    		   btns[2].style.display = "None";
	    		   btns[3].style.display = "None";
    		       break;
    		}  
    	}
    });
}

function bindData(div){
	a = div.parentElement.parentElement.getElementsByTagName("a")[1];
	a.innerHTML = div.value;
	a.href = div.value;
}

function enterURL(div){
	token = document.getElementById("token");
	input = div.parentElement.parentElement.getElementsByTagName("input")[0];
	moduleCode = input.name;
	URL = input.value;
	
	if (URL.trim() === ""){return;}
	
	dataDic = {};
	dataDic[token.name] = token.value;
	dataDic['moduleCode'] = moduleCode;
	dataDic['pendingURL'] = URL;
	
	div.innerHTML = "<span class=\"fa fa-refresh fa-spin\"></span>";
	div.disabled = true;

	// need to send the post request
	rq = $.post( "/gpa/auto/submitURL/", dataDic);
    rq.done(function(data) {
    	btns = document.getElementById("code"+data[1]).getElementsByTagName("button");

    	btns[0].style.display = "None";
    	btns[1].style.display = "None";
    	btns[2].style.display = "None";
    	btns[3].style.display = "None";

    	switch(data[0]){
    		case "PD":
    	    	btns[2].style.display = "inline-block";
    	    	btns[3].style.display = "inline-block";
    			break;
    		case "VWADPD":
    			btns[0].style.display = "inline-block";
    	    	btns[2].style.display = "inline-block";
    	    	btns[3].style.display = "inline-block";
    			break
    	}
    	
    	modalId = "#MarkSheetURL" + data[1];
    	$(modalId).modal("hide");
    	div.innerHTML = "Submit";
    	div.disabled = false;
    });
}

function cancelPending(btn){
	td = btn.parentElement.parentElement;
	module = td.id.slice(4);
	btns = td.getElementsByTagName("button");

	choice="";
	if(btns[0].style.display=="none"){
		choice = "PD";
	}else{
		choice = "VWADPD";
	}
	
	token = document.getElementById("token");
	dataDic = {};
	dataDic[token.name] = token.value;
	dataDic["moduleCode"] = module;
	dataDic["currentStatus"] = choice;
	
	btn.innerHTML = "<span class=\"fa fa-refresh fa-spin\"></span>";
	btn.disabled = true;
	
	rq = $.post( "/gpa/auto/cancelURL/", dataDic);
    rq.done(function(data) {
    	btns[0].style.display = "None";
    	btns[1].style.display = "None";
    	btns[2].style.display = "None";
    	btns[3].style.display = "None";
    	
    	switch(data[0]){
			case "NW":
 			   	btns[1].style.display = "inline-block";
 			   	break;
			case "VWAD":
 			   	btns[0].style.display = "inline-block";
 			   	btns[1].style.display = "inline-block";
 			   	break;
    	}
    	btn.innerHTML = "cancel";
    	btn.disabled = false;
    });
}


