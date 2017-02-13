function loadXMLDoc() {
    var req = new XMLHttpRequest()
    req.onreadystatechange = function() {
        if (req.readyState == 4 && req.status == 200) {
            var response = JSON.parse(req.responseText)
            document.getElementById('myDiv').textContent = "dd";/JSON.stringify(response.dir);//"Temperature: " + response.temp + String.fromCharCode(176) + " F";
            document.getElementById('weatherIcon').src = response.icon_url;
            //Set directions on Google Map
            document.getElementById('travelTime').textContent = response.dir.routes[0].legs[0].duration.text;
            if (!document.getElementById('startloc').value || !document.getElementById('endloc').value) {
                $('#warningMessage').show();
                document.getElementById('warningMessage').textContent = 'Using example directions from Central Park to JFK Airport';
            } else {
                $('#warningMessage').hide();
            }
            directionsDisplay.setDirections(response.dir.routes);
        }
    }

    req.open('POST', '/ajax');
    req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    var dp = document.getElementById('datepicker').value;
    var tp = document.getElementById('timepicker').value;
    var sl = document.getElementById('startloc').value;
    var el = document.getElementById('endloc').value
    var postVars = 'datepicker='+dp+'&timepicker='+tp+'&origin='+sl+'&destination='+el
    req.send(postVars)
    
    return false
}