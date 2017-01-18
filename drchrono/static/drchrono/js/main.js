function ready(fn) {
  if (document.readyState != 'loading') {
    fn();
  } else {
    document.addEventListener('DOMContentLoaded', fn);
  }
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
    console.log('tick');
  });
}

function initTime() {
  document.querySelectorAll('.time').forEach(function(element) {
    displayTimeElement(element);
  });
  window.setInterval(tick, 5);
}

ready(initTime);
