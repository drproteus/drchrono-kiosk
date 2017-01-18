function ready(fn) {
  if (document.readyState != 'loading') {
    fn();
  } else {
    document.addEventListener('DOMContentLoaded', fn);
  }
}

function displayClockElement(element) {
  var seconds = element.dataset['seconds'];
  var hour = Math.floor(seconds/60/60);
  var minute = Math.floor(seconds/60%60);
  var second = Math.floor(seconds%60);
  var meridian = 'PM'
  if (hour < 12) {
    meridian = 'AM';
  } else if (hour == 0) {
    meridian = 'AM';
    hour = 12;
  } else {
    hour = hour % 12;
  }
  element.innerHTML = hour+":"+minute+":"+second+" "+meridian;
}

function tickClocks() {
  document.querySelectorAll('.clock-running').forEach(function(element) {
    element.dataset['seconds'] = (1 + Number(element.dataset['seconds'])) % 86400;
    displayClockElement(element);
  });
}

function initClocks() {
  document.querySelectorAll('.clock').forEach(function(element) {
    displayClockElement(element);
  });
  window.setInterval(tickClocks, 1000);
}

function displayTimeElement(element) {
  var seconds = element.dataset['seconds'];
  var hour = Math.floor(seconds/60/60);
  var minute = Math.floor(seconds/60%60);
  var second = Math.floor(seconds%60);
  element.innerHTML = hour+" Hours, "+minute+" Minutes, "+second+" Second";
  if (second == 0 || second > 1)
    element.innerHTML += "s";
}

function tick() {
  document.querySelectorAll('.time-running').forEach(function(element) {
    element.dataset['seconds'] = 1 + Number(element.dataset['seconds']);
    displayTimeElement(element);
  });
}

function initTime() {
  document.querySelectorAll('.time').forEach(function(element) {
    displayTimeElement(element);
  });
  window.setInterval(tick, 1000);
}

function messageExpiry() {
  window.setTimeout(function() {
    try { 
      fadeOut(document.querySelector('.messages'));
    } catch(err) {}
  }, 5000);
}

function fade(element) {
  element.style['opacity'] = String(Number(element.style['opacity']) - 0.1);
  if (element.style['opacity'] !== '0.0') {
    window.setTimeout(fade, 50, element);
  } else {
    element.remove();
  }
}

function fadeOut(element) {
  element.style['opacity'] = "1.0";
  fade(element);
}

function requestGet(url, success, error) {
  var request = new XMLHttpRequest();
  request.open('GET', url, true);
  request.onload = function() {
    if (request.status >= 200 && request.status < 400) {
      success(request)
    } else {
      error(request)
    }
  }
  request.send();
}

function requestPost(url, data, success, error) {
  var request = new XMLHttpRequest();
  request.open('POST', url, true);
  request.onload = function() {
    if (request.status >= 200 && request.status < 400) {
      success(request)
    } else {
      error(request)
    }
  }
  request.send(data);
}

function insertAfter(element, after) {
  element.parentNode.insertBefore(after, element.nextSibling);
}

function insertBefore(element, before) {
  element.parentNode.insertBefore(before, element);
}

function updateWaitTimeDiv(newText) {
  document.querySelector('.waiting-time').innerHTML = newText;
  displayTimeElement(document.querySelector('.waiting-time .time'));
}

function updateAverageLoop() {
  window.setInterval(function() {
    requestGet('http://localhost:8000/wait_time/', function(request) {
      updateWaitTimeDiv(request.responseText);
    }, function(request) {
      console.log(request);
    });
  }, 5000);
}

function refreshArrivals() {
  var arrivalsList = document.querySelector('ul.arrivals');
  if (arrivalsList !== null) {
    requestGet('http://localhost:8000/arrivals/', function(request) {
      arrivalsList.innerHTML = request.responseText;
      arrivalsList.querySelectorAll('.time').forEach(function(element) {
        displayTimeElement(element);
      });
    }, function(request) { console.log('Failed to get arrivals.')});
  }
}

Notification.requestPermission().then(function(result) {
  console.log(result);
});

function newNotification(body, icon) {
  if (window.notifications === undefined) {
    window.notifications = [];
  }
  var options = {
    body: body,
    icon: icon, 
  }
  var n = new Notification('New Check-In', options);
  window.notifications.push(n);
  n.onclick = function() {
    window.notifications.forEach(function(item) {
      item.close();
    });
    window.location = 'http://localhost:8000/dashboard/';
  }
}

function arrivalNotifyLoop() {
  window.setInterval(function() {
    var data = {};
    requestGet('http://localhost:8000/check_if_new/', function(request) {
      data = JSON.parse(request.response);
      if (data['new_arrival_count'] > 0) {
        data['new_arrivals'].forEach(function(arrival) {
         newNotification(arrival['patient_name'] + " checked-in for their " + arrival['scheduled_time'] + " at " + arrival['checked_in'] + ".", arrival['patient_photo']);
        });
        refreshArrivals();
      }
    }, function() {  });
  }, 5000);
}

// prepare functions for running onload
ready(messageExpiry);
