//Windy
const options = {
    // Required: API key
    key: 'x1PZYs950IBWv2zNFKUElc2IcN0sbfyl', // REPLACE WITH YOUR KEY !!!

    // Put additional console output
    verbose: false,

    // Optional: Initial state of the map
    lat: 10,
    lon: 81.8262,
    zoom: 5,
};

// Initialize Windy API


windyInit(options, windyAPI => {
    // windyAPI is ready, and contain 'map', 'store',
    // 'picker' and other usefull stuff

    const {map}  = windyAPI;
    // .map is instance of Leaflet map
    document.getElementById("map-button").addEventListener("click", function(){
        let lat = document.getElementById("f1").value;
        let lng = document.getElementById("f2").value;
        map.panTo(new L.LatLng(lat, lng));
        L.popup()
        .setLatLng(new L.LatLng(lat, lng))
        .setContent('Latitude: ' + lat + '  Longitude: '  + lng)
        .openOn(map);
    });
});

function flag() {
var toastTrigger = document.getElementById('liveToastBtn')
var toastLiveExample = document.getElementById('liveToast')
if (toastTrigger) {
  toastTrigger.addEventListener('click', function () {
    var toast = new bootstrap.Toast(toastLiveExample)

    toast.show()
  })
}
}

//Make it rain
var makeItRain = function(r) {
  //clear out everything
  if(r==1){
  return;
  }
  flag();
  document.getElementById('liveToastBtn').click();
  $('.rain').empty();

  var increment = 0;
  var drops = "";
  var backDrops = "";

  while (increment < r) {
    //couple random numbers to use for various randomizations
    //random number between 98 and 1
    var randoHundo = (Math.floor(Math.random() * (98 - 1 + 1) + 1));
    //random number between 5 and 2
    var randoFiver = (Math.floor(Math.random() * (5 - 2 + 1) + 2));
    //increment
    increment += randoFiver;
    //add in a new raindrop with various randomizations to certain CSS properties
    drops += '<div class="drop" style="left: ' + increment + '%; bottom: ' + (randoFiver + randoFiver - 1 + 100) + '%; animation-delay: 0.' + randoHundo + 's; animation-duration: 0.5' + randoHundo + 's;"><div class="stem" style="animation-delay: 0.' + randoHundo + 's; animation-duration: 0.5' + randoHundo + 's;"></div><div class="splat" style="animation-delay: 0.' + randoHundo + 's; animation-duration: 0.5' + randoHundo + 's;"></div></div>';
    backDrops += '<div class="drop" style="right: ' + increment + '%; bottom: ' + (randoFiver + randoFiver - 1 + 100) + '%; animation-delay: 0.' + randoHundo + 's; animation-duration: 0.5' + randoHundo + 's;"><div class="stem" style="animation-delay: 0.' + randoHundo + 's; animation-duration: 0.5' + randoHundo + 's;"></div><div class="splat" style="animation-delay: 0.' + randoHundo + 's; animation-duration: 0.5' + randoHundo + 's;"></div></div>';
  }

  $('.rain.front-row').append(drops);
  $('.rain.back-row').append(backDrops);
}

$('.splat-toggle.toggle').on('click', function() {
  $('.rain-effect').toggleClass('splat-toggle');
  $('.splat-toggle.toggle').toggleClass('active');
  makeItRain();
});