function SGPA(){
    var map = {'A+':4.2, 'A':4.0, 'A-':3.7, 'B+':3.3, 'B':3.0, 'B-':2.7, 'C+':2.3, 'C':2.0, 'C-':1.5, 'D':1.0, 'F':0.0};
    var grade = document.getElementsByTagName('select');
    var credit = document.getElementsByName('cred');
    
    var total = 0;
    var credits = 0;
    for (var x=0; x<grade.length; x++){
    
        var points = map[grade[x].options[grade[x].selectedIndex].value]
        
        if (points!=undefined){
            total += points*parseFloat(credit[x].innerText);
            credits += parseFloat(credit[x].innerText);
        }
    }
    document.getElementById('output').innerText = 'NEW SGPA : '+(total/credits).toFixed(4);
}
