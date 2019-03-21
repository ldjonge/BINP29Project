function showLong() {
  var linShort = document.getElementById("lineageShort");
  var linLong = document.getElementById("lineageLong");
  linShort.style.display = 'none';
  linLong.style.display = 'block';
};

function showShort() {
  var linShort = document.getElementById("lineageShort");
  var linLong = document.getElementById("lineageLong");
  linShort.style.display = 'block';
  linLong.style.display = 'none';
}
