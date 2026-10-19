(function () {
  "use strict";
  var button = document.getElementById("print-resume");
  if (!button) return;
  button.hidden = false;
  button.addEventListener("click", function () {
    window.print();
  });
}());
