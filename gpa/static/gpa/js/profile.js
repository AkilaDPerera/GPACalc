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