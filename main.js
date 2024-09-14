window.addEventListener("DOMContentLoaded", function () {
    // get the form elements defined in your form HTML above
  
    var form = document.getElementById("my-form");
    var status = document.getElementById("status");
  
    // Success and Error functions for after the form is submitted
  
    function success() {
      form.reset();
      status.classList.add("success");
      status.innerHTML = "Thanks!";
    }
  
    function error() {
      status.classList.add("error");
      status.innerHTML = "Oops! There was a problem.";
    }
  
    // handle the form submission event
  
    form.addEventListener("submit", function (ev) {
      ev.preventDefault();
      var data = new FormData(form);
      ajax(form.method, form.action, data, success, error);
    });
  });
  
  // helper function for sending an AJAX request
  
  function ajax(method, url, data, success, error) {
    var xhr = new XMLHttpRequest();
    xhr.open(method, url);
    xhr.setRequestHeader("Accept", "application/json");
    xhr.onreadystatechange = function () {
      if (xhr.readyState !== XMLHttpRequest.DONE) return;
      if (xhr.status === 200) {
        success(xhr.response, xhr.responseType);
      } else {
        error(xhr.status, xhr.response, xhr.responseType);
      }
    };
    xhr.send(data);
  }
  
  var map = L.map('mapid').setView([51.2538, -85.3232], 5);
	//L.tileLayer('//{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
	L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoiYWp1dHppIiwiYSI6ImNrbGQ3d2E4MTE3cHAydXFlanJ1aG9maG4ifQ.6MOuQtvruOzh95-1C3i0jg', {
			attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
			maxZoom: 19,
			id: 'mapbox/streets-v11',
			tileSize: 512,
			zoomOffset: -1,
			accessToken: 'pk.eyJ1IjoiYWp1dHppIiwiYSI6ImNrbGQ3d2E4MTE3cHAydXFlanJ1aG9maG4ifQ.6MOuQtvruOzh95-1C3i0jg'
		}).addTo(map);
	
	/* locationiq geocoding
	//Geocoder options
	var geocoderControlOptions = {
		bounds: false,          //To not send viewbox
		markers: false,         //To not add markers when we geocoder
		attribution: null,      //No need of attribution since we are not using maps
		expanded: true,         //The geocoder search box will be initialized in expanded mode
		panToPoint: false       //Since no maps, no need to pan the map to the geocoded-selected location
	}
	//Initialize the geocoder
	var geocoderControl = new L.control.geocoder('pk.e5dcd9a634448df3e8c1ff3b1515c793', geocoderControlOptions).addTo(map).on('select', function (e) {
		displayLatLon(e.feature.feature.display_name, e.latlng.lat, e.latlng.lng);
	});
	*/

   
  
/*
    var baseMaps = {
      "Street": Street,
      "Satellite": Satellite,
      'Outdoors': Outdoors
     
  };

  var Temperature = (new L.tileLayer("http://tile.openweathermap.org/map/temp_new/{z}/{x}/{y}.png?appid=6a7e01daf992d16cd943dae3b79d1550")),
    wind = (new L.tileLayer("http://tile.openweathermap.org/map/wind_new/{z}/{x}/{y}.png?appid=6a7e01daf992d16cd943dae3b79d1550"));

    var overlays = {
  "Air Temperature" : Temperature,
  "Wind Speed" : wind,
  };
  //L.control.layers(baseMaps, overlays, {collapsed:true}).addTo(map);
   
      

  map.on('mousemove click', function(e) {
    //window[e.type].innerHTML = e.containerPoint.toString() + ', ' + e.latlng.toString();
    window[e.type].innerHTML = e.latlng.toString();
    
});
  */
 
		function roundUp(x, num)
		{
			return Math.ceil(x/num)*num;
		}
		
		var customFloor = function(value, roundTo) {
		return Math.floor(value / roundTo) * roundTo;
		}
		
		var theMarker = {};
		
		
		window.ft1 == 'empty';
		window.mw1 == 'empty';
		
		map.on('click',function(e){
			console.log("You clicked the map at LAT: "+ e.latlng.lat+" and LONG: "+e.latlng.lon );
					//Clear existing marker, 

					if (theMarker != undefined) {
						  map.removeLayer(theMarker);
					};

				//Add a marker to show where you clicked.
				 theMarker = L.marker([e.latlng.lat,e.latlng.lng]).addTo(map);
		});
		
		map.on('click', function(layer){
		  var latlng = map.mouseEventToLatLng(layer.originalEvent);
		  console.log(latlng.lat + ', ' + latlng.lng);
		  //console.log('lat round down: ' + (Math.floor(latlng.lat * 10)/10) + ' lon round down: ' + (Math.floor(latlng.lng * 10)/10));
		  //console.log('lat round up: ' + (Math.round(latlng.lat * 10)/10) + ' lon round up: ' + (Math.round(latlng.lng * 10)/10));
		  //console.log(String(customFloor((latlng.lng), 0.4)).replace(".","").replace("-","") + String(RoundTo((latlng.lat), 0.4)).replace(".","") 
		  //+ String(RoundTo((latlng.lng), 0.4)).replace(".","").replace("-","") + String(customFloor((latlng.lat), 0.4)).replace(".",""));
		  
		  
		  
		  
		  
		  
		  
		  var left = (String(customFloor((latlng.lng), 0.4)).replace(".","").replace("-","")).substring(0,3),
		  top =  (String(roundUp((latlng.lat), 0.4)).replace(".","").substring(0,3)),
		  right = (String(roundUp((latlng.lng), 0.4)).replace(".","").replace("-","")).substring(0,3),
		  bottom = (String(customFloor((latlng.lat), 0.4)).replace(".","")).substring(0,3);
		  
		  console.log('left: ' + left);
		  console.log('top: ' + top);
		  console.log('right: ' + right);
		  console.log('bottom: ' + bottom);
		  console.log('grid_tilename_G' + left + top + right + bottom);
		  tile = left + top + right + bottom
		  
		  
		  
		  $.get( "https://arubrum.ca:50780/documents/grid_tilename_G" + tile + ".geojson", function( data ) {
		  //https://raw.githubusercontent.com/aaronjutzi/Fahrenheit2101/main/grid_tilename_G792448788444.geojson
		  
		  //console.log(data);
		  //var obj  = JSON.stringify(data);
		  var obj = JSON.parse(data);
		  
		  
		  console.log(obj.features.length);
		  
		  obj_len = obj.features.length;
		  d = 'empty'
		  for (i = 0; i < obj_len; i++){
			
			console.log('b: ' + (obj.features[i].properties.top - latlng.lat));
			console.log('c: ' + (obj.features[i].properties.left - latlng.lng));
			
			b = obj.features[i].properties.top - latlng.lat;
			c = obj.features[i].properties.left - latlng.lng;
			
			console.log(Math.sqrt((b**2) + (c**2)));
			
			a = Math.sqrt((b**2) + (c**2))
			
			
			if (d !== 'empty') {
				if (a < d){
				d = a;
				x = i;} else {
				d = d;}
			} else {
			d = a
			x = i}
			}
			
			
			
		  
		  console.log('d: ' + d);
		  console.log('i: ' + x);
		  
		  console.log(obj.features[0].properties.left);
		  console.log(obj.features[0].properties.top);
		  
		  
		  window.t0 = obj.features[x].properties.t01.toFixed(0),
			  window.t1 = obj.features[x].properties.t11.toFixed(0),
			  window.t2 = obj.features[x].properties.t21.toFixed(0),
			  window.t3 = obj.features[x].properties.t31.toFixed(0),
			  window.t4 = obj.features[x].properties.t41.toFixed(0),
			  window.t5 = obj.features[x].properties.t51.toFixed(0),
			  window.w0 = obj.features[x].properties.w01.toFixed(0),
			  window.w1 = obj.features[x].properties.w11.toFixed(0),
			  window.w2 = obj.features[x].properties.w21.toFixed(0),
			  window.w3 = obj.features[x].properties.w31.toFixed(0),
			  window.w4 = obj.features[x].properties.w41.toFixed(0),
			  window.w5 = obj.features[x].properties.w51.toFixed(0);
		  
		  window.lat = latlng.lat.toFixed(5);
		  window.lon = latlng.lng.toFixed(5);
		  
		  /*document.getElementById("temp").innerHTML = "Marker coordinates: " + latlng.lat.toFixed(5) + ', ' + latlng.lng.toFixed(5) + "<br />" +
		  "Temp: " + t0 + "<br />" +
		  //((obj.features[x].properties.t01 * 1.8) + 32).toFixed(2) + "&#176;F" + "<br />" +
		  //"Wind Speed: " + obj.features[x].properties.w01.toFixed(2) + " KM/H" + "<br />" +
		  //(obj.features[x].properties.w01 / 1.609344).toFixed(2) + " MPH"
		  //+ "<br />" +
		  "1 " + t1 + "&#176;C" + "<br />" +
		  "2 " + t2 + "&#176;C"+ "<br />" +
		  "3 " + t3 + "&#176;C"+ "<br />" +
		  "4 " + t4 + "&#176;C"+ "<br />" +
		  "5 " + t5 + "&#176;C";
		  
		  document.getElementById("wind").innerHTML =
		  "1 " + w1 + " KM/H"+ "<br />" +
		  "2 " + w2 + " KM/H"+ "<br />" +
		  "3 " + w3 + " KM/H"+ "<br />" +
		  "4 " + w4 + " KM/H"+ "<br />" +
		  "5 " + w5 + " KM/H"; */
		  
		  document.getElementById("t0").innerHTML = obj.features[x].properties.t01.toFixed(0) + "&#176;C";
		  document.getElementById("t1").innerHTML = obj.features[x].properties.t11.toFixed(0) + "&#176;C";
		  document.getElementById("t2").innerHTML = obj.features[x].properties.t21.toFixed(0) + "&#176;C";
		  document.getElementById("t3").innerHTML = obj.features[x].properties.t31.toFixed(0) + "&#176;C";
		  document.getElementById("t4").innerHTML = obj.features[x].properties.t41.toFixed(0) + "&#176;C";
		  document.getElementById("t5").innerHTML = obj.features[x].properties.t51.toFixed(0) + "&#176;C";
		  
		  document.getElementById("w0").innerHTML = obj.features[x].properties.w01.toFixed(0) + " KM/H";
		  document.getElementById("w1").innerHTML = obj.features[x].properties.w11.toFixed(0) + " KM/H";
		  document.getElementById("w2").innerHTML = obj.features[x].properties.w21.toFixed(0) + " KM/H";
		  document.getElementById("w3").innerHTML = obj.features[x].properties.w31.toFixed(0) + " KM/H";
		  document.getElementById("w4").innerHTML = obj.features[x].properties.w41.toFixed(0) + " KM/H";
		  document.getElementById("w5").innerHTML = obj.features[x].properties.w51.toFixed(0) + " KM/H"; 
		  
		});
		});
		
		function tcon() {
		  /*document.getElementById('temp').innerHTML = 
		  ((t0 * 1.8) + 32).toFixed(2) + "&#176;F" + "<br />" +
		  ((t1 * 1.8) + 32).toFixed(2) + "&#176;F" + "<br />" +
		  ((t2 * 1.8) + 32).toFixed(2) + "&#176;F"+ "<br />" +
		  ((t3 * 1.8) + 32).toFixed(2) + "&#176;F"+ "<br />" +
		  ((t4 * 1.8) + 32).toFixed(2) + "&#176;F"+ "<br />" +
		  ((t5 * 1.8) + 32).toFixed(2) + "&#176;F";
		  
		 
		  window.ft0 = ((t1 * 1.8) + 32).toFixed(2)
		  window.ft1 = ((t1 * 1.8) + 32).toFixed(2)
		  window.ft2 = ((t2* 1.8) + 32).toFixed(2) 
		  window.ft3 = ((t3* 1.8) + 32).toFixed(2)
		  window.ft4 = ((t4* 1.8) + 32).toFixed(2)
		  window.ft5 = ((t5* 1.8) + 32).toFixed(2);*/
		  
		  document.getElementById("t0").innerHTML = ((t0 * 1.8) + 32).toFixed(0) + "&#176;F";
		  document.getElementById("t1").innerHTML = ((t1 * 1.8) + 32).toFixed(0) + "&#176;F";
		  document.getElementById("t2").innerHTML = ((t2 * 1.8) + 32).toFixed(0) + "&#176;F";
		  document.getElementById("t3").innerHTML = ((t3 * 1.8) + 32).toFixed(0) + "&#176;F";
		  document.getElementById("t4").innerHTML = ((t4 * 1.8) + 32).toFixed(0) + "&#176;F";
		  document.getElementById("t5").innerHTML = ((t5 * 1.8) + 32).toFixed(0) + "&#176;F";
		  
		  window.ft0 = ((t0 * 1.8) + 32).toFixed(0)
		  window.ft1 = ((t1 * 1.8) + 32).toFixed(0)
		  window.ft2 = ((t2* 1.8) + 32).toFixed(0) 
		  window.ft3 = ((t3* 1.8) + 32).toFixed(0)
		  window.ft4 = ((t4* 1.8) + 32).toFixed(0)
		  window.ft5 = ((t5* 1.8) + 32).toFixed(0);
		  
		}
		
		function ccon() {
		
			if (ft1 !== 'empty'){
		  /*document.getElementById('temp').innerHTML = 
		  "0 " + ((ft0 - 32) * (5/9)).toFixed(2) + "&#176;C" + "<br />" +
		  "1 " + ((ft1 - 32) * (5/9)).toFixed(2) + "&#176;C" + "<br />" +
		  "2 " + ((ft2 - 32) * (5/9)).toFixed(2) + "&#176;C"+ "<br />" +
		  "3 " + ((ft3 - 32) * (5/9)).toFixed(2) + "&#176;C"+ "<br />" +
		  "4 " + ((ft4 - 32) * (5/9)).toFixed(2) + "&#176;C"+ "<br />" +
		  "5 " + ((ft5 - 32) * (5/9)).toFixed(2) + "&#176;C";*/
		  
		   document.getElementById("t0").innerHTML = ((ft0 - 32) * (5/9)).toFixed(0) + "&#176;C";
		  document.getElementById("t1").innerHTML = ((ft1 - 32) * (5/9)).toFixed(0) + "&#176;C";
		  document.getElementById("t2").innerHTML = ((ft2 - 32) * (5/9)).toFixed(0) + "&#176;C";
		  document.getElementById("t3").innerHTML = ((ft3 - 32) * (5/9)).toFixed(0) + "&#176;C";
		  document.getElementById("t4").innerHTML = ((ft4 - 32) * (5/9)).toFixed(0) + "&#176;C";
		  document.getElementById("t5").innerHTML = ((ft5 - 32) * (5/9)).toFixed(0) + "&#176;C";
		  
		  window.ft1 == 'empty';
		}
	
		}
		
		
		function mcon() {
		
		  /*document.getElementById("wind").innerHTML =
		  "0 " + (w0 / 1.609344).toFixed(2) + " MPH"+ "<br />" +
		  "1 " + (w1 / 1.609344).toFixed(2) + " MPH"+ "<br />" +
		  "2 " + (w2 / 1.609344).toFixed(2) + " MPH"+ "<br />" +
		  "3 " + (w3 / 1.609344).toFixed(2) + " MPH"+ "<br />" +
		  "4 " + (w4 / 1.609344).toFixed(2) + " MPH"+ "<br />" +
		  "5 " + (w5 / 1.609344).toFixed(2) + " MPH"; 
		
			window.mw0 = (w1 / 1.609344).toFixed(2)
			window.mw1 = (w1 / 1.609344).toFixed(2)
		  window.mw2 = (w2 / 1.609344).toFixed(2) 
		  window.mw3 = (w3 / 1.609344).toFixed(2)
		  window.mw4 = (w4 / 1.609344).toFixed(2)
		  window.mw5 = (w5 / 1.609344).toFixed(2);*/
		  
		  document.getElementById("w0").innerHTML = (w0 / 1.609344).toFixed(0) + " MPH";
		  document.getElementById("w1").innerHTML = (w1 / 1.609344).toFixed(0) + " MPH";
		  document.getElementById("w2").innerHTML = (w2 / 1.609344).toFixed(0) + " MPH";
		  document.getElementById("w3").innerHTML = (w3 / 1.609344).toFixed(0) + " MPH";
		  document.getElementById("w4").innerHTML = (w4 / 1.609344).toFixed(0) + " MPH";
		  document.getElementById("w5").innerHTML = (w5 / 1.609344).toFixed(0) + " MPH"; 
		  
		  window.mw0 = (w0 / 1.609344).toFixed(0)
			window.mw1 = (w1 / 1.609344).toFixed(0)
		  window.mw2 = (w2 / 1.609344).toFixed(0) 
		  window.mw3 = (w3 / 1.609344).toFixed(0)
		  window.mw4 = (w4 / 1.609344).toFixed(0)
		  window.mw5 = (w5 / 1.609344).toFixed(0);
		  
		}
		
		
		
		function kcon() {
		
			if (mw1 !== 'empty'){
		  /*document.getElementById("wind").innerHTML =
		  "0 " + (mw0 * 1.609344).toFixed(2) + " KM/H"+ "<br />" +
		  "1 " + (mw1 * 1.609344).toFixed(2) + " KM/H"+ "<br />" +
		  "2 " + (mw2 * 1.609344).toFixed(2) + " KM/H"+ "<br />" +
		  "3 " + (mw3 * 1.609344).toFixed(2) + " KM/H"+ "<br />" +
		  "4 " + (mw4 * 1.609344).toFixed(2) + " KM/H"+ "<br />" +
		  "5 " + (mw5 * 1.609344).toFixed(2) + " KM/H"; */
		  
		  document.getElementById("w0").innerHTML = (mw0 * 1.609344).toFixed(0) + " KM/H";
		  document.getElementById("w1").innerHTML = (mw1 * 1.609344).toFixed(0) + " KM/H";
		  document.getElementById("w2").innerHTML = (mw2 * 1.609344).toFixed(0) + " KM/H";
		  document.getElementById("w3").innerHTML = (mw3 * 1.609344).toFixed(0) + " KM/H";
		  document.getElementById("w4").innerHTML = (mw4 * 1.609344).toFixed(0) + " KM/H";
		  document.getElementById("w5").innerHTML = (mw5 * 1.609344).toFixed(0) + " KM/H"; 
		   
		  
		  window.mw1 == 'empty';
		}
	
		}
		
		
		  var d = new Date();
		  var n = d.getHours();
		  
		  if ((Number(n) + 1) >= 24){
		  n1 = ((Number(n) + 1) - 24)}
		  else {
		  n1 = (Number(n) + 1) 
		  };
		  
		  if ((Number(n) + 2) >= 24){
		  n2 = ((Number(n) + 2) - 24)}
		  else {
		  n2 = (Number(n) + 2) 
		  };
		  
		  if ((Number(n) + 3) >= 24){
		  n3 = ((Number(n) + 3) - 24)}
		  else {
		  n3 = (Number(n) + 3) 
		  };
		  
		  if ((Number(n) + 4) >= 24){
		  n4 = ((Number(n) + 4) - 24)}
		  else {
		  n4 = (Number(n) + 4) 
		  };
		  
		  if ((Number(n) + 5) >= 24){
		  n5 = ((Number(n) + 5) - 24)}
		  else {
		  n5 = (Number(n) + 5) 
		  };
		  
		  
		  document.getElementById("ho0").innerHTML = n + ":00";
		  document.getElementById("ho1").innerHTML = n1 + ":00";
		  document.getElementById("ho2").innerHTML = n2 + ":00";
		  document.getElementById("ho3").innerHTML = n3 + ":00";
		  document.getElementById("ho4").innerHTML = n4 + ":00";
		  document.getElementById("ho5").innerHTML = n5 + ":00";
		
		  document.getElementById("ho0w").innerHTML = n + ":00";
		  document.getElementById("ho1w").innerHTML = n1 + ":00";
		  document.getElementById("ho2w").innerHTML = n2 + ":00";
		  document.getElementById("ho3w").innerHTML = n3 + ":00";
		  document.getElementById("ho4w").innerHTML = n4 + ":00";
		  document.getElementById("ho5w").innerHTML = n5 + ":00";
		  
		  
		  /*map.locate({setView: true, maxZoom: 16});
		  
		  function onLocationFound(e) {
				var radius = e.accuracy;

				L.marker(e.latlng).addTo(map)
					.bindPopup("You are within " + radius + " meters from this point").openPopup();
					closePopupOnClick: true;
				L.circle(e.latlng, radius).addTo(map);
			}

			map.on('locationfound', onLocationFound); */
			
			
			var locator = L.control.locate({
				closePopupOnClick: true,
				position: 'topright'
				}).addTo(map);
			
			
			//function onLocationError(e) {
			//	alert(e.message);
			//}

			//map.on('locationerror', onLocationError);



			L.Control.geocoder().addTo(map);

			// Creating variables for weather tile layers
        // OpenWeatherMap API tile reference: https://openweathermap.org/api/weathermaps
        // Leaflet tile reference: https://leafletjs.com/reference-1.7.1.html#tilelayer
        // Javascript 'new' operator reference: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/new
		var precip = (new L.TileLayer("http://tile.openweathermap.org/map/precipitation_new/{z}/{x}/{y}.png?appid=35b79f04000d801c24276115e7093f38")),
			clouds = (new L.TileLayer("http://tile.openweathermap.org/map/clouds_new/{z}/{x}/{y}.png?appid=35b79f04000d801c24276115e7093f38"));
		
		    
        // Key-value pairs used for the control panel 
        // Keys are the text values seen in the control panel, and the values are the corresponding tile layer variables
        // Layer groups and layers control tutorial: https://leafletjs.com/examples/layers-control/
		var overlayMaps = {
		"Precipitation" : precip,
		"Clouds" : clouds
	
		};
		//map.locate({setView: true, maxZoom: 16});
		
        // Control panel in top left corner
        // Gives user the ability to toggle between different weather layers
		L.control.layers("",overlayMaps).addTo(map);
		
		
		/*
		var geojsonFeature = {
			"type": "Feature",
			"properties": {
				"name": "Coors Field",
				"amenity": "Baseball Stadium",
				"popupContent": "This is where the Rockies play!"
			},
			"geometry": {
				"type": "Point",
				"coordinates": [-104.99404, 39.75621]
			}
		};
		
		var geojsonLayer = new L.GeoJSON.AJAX("https://arubrum.ca:50780/main/on_merc.geojson");       
		var polygon = L.polygon(geojsonLayer, {color: 'red'}).addTo(map);
		
		var geojsonLayer2 = new L.GeoJSON.AJAX("https://arubrum.ca:50780/documents/grid_tilename_G832472828468.geojson");       
		geojsonLayer2.addTo(map);
		*/
		
		
		
				
