var table;
var data;
$(document).ready(function() {
	$('#batchBtn').click(function(event) {
		var isvalidate = $("#reportForm")[0].checkValidity();
	    if (isvalidate) {
	      event.preventDefault();
		    //Ajax request
		    var batch = document.getElementById("batch").value;
		    var dptm = document.getElementById("dptm").value;
		    var token = document.getElementById("token").value;
		    document.getElementById("spinner").innerHTML = "<div class=\"loading\">Loading&#8230;</div>";
		    var posting = $.post( "/gpa/reports/getReportData/", {batch: batch, dptm: dptm, csrfmiddlewaretoken: token} );
		    
		    posting.done(function(d){
		    	google.charts.load('current', {'packages':['table']});
		    	google.charts.setOnLoadCallback(drawTable);
		    	
		    	function drawTable() {
		     		data = new google.visualization.DataTable();
		    		for (var heading in d[0]){
		    			data.addColumn('string', d[0][heading]);
		    		}
		    		data.addRows(d[1]);
		    		
				 	table = new google.visualization.Table(document.getElementById('table_div'));
				  	table.draw(data, {showRowNumber: true, width: '100%', height: '100%'});
				  	google.visualization.events.addListener(table, 'select', selectHandler);
		    	}
		    	document.getElementById("spinner").innerHTML = "";
		    })
	    }
	})
});

var clicks = 0;
var row;
var username;
function selectHandler(event){
	if (!(table.getSelection()[0]===undefined)){
		row = table.getSelection()[0].row;
		username = data.getFormattedValue(row, 0);
	}
	clicks++;
	setTimeout(function() {
		if (clicks >= 2) {
//			location.assign("/gpa/reports/"+username);
			window.open("/gpa/reports/"+username+"/");
			}
		clicks = 0;
		}, 250);
}
