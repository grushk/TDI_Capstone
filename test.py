<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
    <title>Traffic Prediction</title>

    <!-- Bootstrap -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
    <link href="../static/css/custom.css" rel="stylesheet">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
    <script type="text/javascript">
        Date.prototype.toDateInputValue = (function() {
            var local = new Date(this);
            local.setMinutes(this.getMinutes() - this.getTimezoneOffset());
            return local.toJSON();
        });

        function initializeTimes() {
            document.getElementById('datepicker').value = new Date().toDateInputValue().slice(0,10);
            document.getElementById('timepicker').value = new Date().toDateInputValue().slice(11,16);
        }
        window.onload = initializeTimes;
    </script>
    <script type="text/javascript">
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
    </script>
</head>
<body>
    <nav class="navbar navbar-fixed-top navbar-inverse">
        <div class="container-fluid">
            <div class="navbar-header">
                <button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#navbar">
                    <span class="sr-only">Toggle navigation</span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                </button>
                <a class="navbar-brand" href="/">Weather Based Traffic Modeling</a>
            </div>
            <div id="navbar" class="navbar-collapse collapse">
                <ul class="nav navbar-nav">
                    <li class="active"><a href="/">Home</a></li>
                    <li><a href="/analysis">Exploratory Analysis</a></li>
                </ul>
            </div>
        </div>
    </nav>
    <div class="container-fluid">
        <div class="col-xs-5 col-md-4 sidebar">
            <label for="startloc">Travel Time Prediction</label>
            <div class="input-group">
                <span class="input-group-addon" id="basic-addon1"><span class="glyphicon glyphicon-map-marker"></span></span>
                <input type="text" id="startloc" placeholder="Starting point" class="form-control" aria-describedby="basic-addon1">
            </div><br>
            <div class="input-group">
                <span class="input-group-addon" id="basic-addon2"><span class="glyphicon glyphicon-map-marker"></span></span>
                <input type="text" id="endloc" placeholder="Ending point" class="form-control" aria-describedby="basic-addon2">
            </div><br>
            
            <label for="date">Departure Time</label>
            <div class="input-group">
                <span class="input-group-addon" id="basic-addon3"><span class="glyphicon glyphicon-calendar"></span></span>
                <input type="date" class="form-control" id="datepicker" aria-describedby="basic-addon3">
            </div><br>
            <div class="input-group">
                <span class="input-group-addon" id="basic-addon4"><span class="glyphicon glyphicon-time"></span></span>
                <input type="time" class="form-control" id="timepicker" aria-describedby="basic-addon4">
            </div><br>
            <input class="btn btn-primary btn-block" type="submit" value="Submit" onclick="return loadXMLDoc()">
        </div>
        
        <div class="col-xs-7 col-xs-offset-5 col-md-8 col-md-offset-4 main">
            <div class="jumbotron">
                Predicted Travel Time:
                <span id="travelTime"></span>
                <div id="warningMessage" class="alert alert-danger" role="alert" style="display: none;"></div>

                <img src="" id="weatherIcon">
                <div id="myDiv"></div>
            </div>
            <div id="map" class="col-md-12" style="height:500px"></div>
        </div>
    </div>



    <script>
        function initMap() {
            var directionsService = new google.maps.DirectionsService;
            var directionsDisplay = new google.maps.DirectionsRenderer;
            var map = new google.maps.Map(document.getElementById('map'), {
                zoom: 10,
                center: {lat: 40.713639, lng: -73.997265}
            });
            directionsDisplay.setMap(map);

            var onChangeHandler = function() {
                if(document.getElementById('startloc').value != "" && document.getElementById('endloc').value != "") {
                    calculateAndDisplayRoute(directionsService, directionsDisplay);
                    //sgetWeatherResults();
                }
            };
            //document.getElementById('startloc').addEventListener('blur', onChangeHandler);
            //document.getElementById('endloc').addEventListener('blur', onChangeHandler);
        }

        function calculateAndDisplayRoute(directionsService, directionsDisplay) {
            directionsService.route({
                origin: document.getElementById('startloc').value,
                destination: document.getElementById('endloc').value,
                travelMode: 'DRIVING'
            }, function(response, status) {
                if (status === 'OK') {
                    $('#warningMessage').hide();
                    directionsDisplay.setDirections(response);
                    //var obj = JSON.parse(response);
                    document.getElementById('travelTime').textContent = response.routes[0].legs[0].duration.text;
                } else {
                    $('#warningMessage').show();
                    document.getElementById('warningMessage').textContent = 'Directions request failed due to ' + status;
                }
            });
        }
        function getWeatherResults() {
            
            //$.getJSON('http://api.wunderground.com/api/784ea582c4d13bc7/hourly10day/q/NY/New_York_City.json', function(data) {

            //});
        }
    </script>
    <script async defer
    src="https://maps.googleapis.com/maps/api/js?key={{ gmaps_key }}&callback=initMap">
    </script>
    <script type="text/javascript">
        var placeSearch,autocomplete;

        function initAutocomplete() {
            autocomplete = new google.maps.places.Autocomplete(document.getElementById('startloc'), { types: [ 'geocode' ] });
            google.maps.event.addListener(autocomplete, 'place_changed', function() {
                fillInAddress();
                //calculateAndDisplayRoute(directionsService, directionsDisplay);
            });
            autocomplete2 = new google.maps.places.Autocomplete(document.getElementById('endloc'), { types: [ 'geocode' ] });
            google.maps.event.addListener(autocomplete2, 'place_changed', function() {
                fillInAddress();
                //calculateAndDisplayRoute(directionsService, directionsDisplay);
            });
            initMap();
        }
        function fillInAddress() {
            var place = autocomplete.getPlace();

            for (var component in component_form) {
                document.getElementById(component).value = "";
                document.getElementById(component).disabled = false;
            }

            for (var j = 0; j < place.address_components.length; j++) {
                var att = place.address_components[j].types[0];
                if (component_form[att]) {
                    var val = place.address_components[j][component_form[att]];
                    document.getElementById(att).value = val;
                }
            }
        }
    </script>
    <script src="https://maps.googleapis.com/maps/api/js?key={{ gmaps_key }}&libraries=places&callback=initAutocomplete"
         async defer></script>
    <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
    <!--script src="http://cdnjs.cloudflare.com/ajax/libs/jquery/1.12.1/jquery.min.js"script-->
</body>
</html>