(function () {
  "use strict";
  var navigation = document.getElementById("navigation");
  var toggle = document.querySelector(".navbar-toggler");
  if (!navigation || !toggle) return;
  var desktop = window.matchMedia("(min-width: 992px)");

  function setExpanded(expanded) {
    toggle.setAttribute("aria-expanded", String(expanded));
    toggle.setAttribute("aria-label", expanded ? "Close navigation" : "Open navigation");
    navigation.hidden = !expanded;
  }
  function syncViewport() {
    if (desktop.matches && document.activeElement === toggle) {
      navigation.querySelector("a").focus();
    } else if (!desktop.matches && navigation.contains(document.activeElement)) {
      toggle.focus();
    }
    toggle.hidden = desktop.matches;
    setExpanded(desktop.matches);
  }
  toggle.addEventListener("click", function () {
    setExpanded(toggle.getAttribute("aria-expanded") !== "true");
  });
  navigation.addEventListener("keydown", function (event) {
    if (event.key === "Escape" && !desktop.matches) {
      setExpanded(false);
      toggle.focus();
    }
  });
  navigation.addEventListener("click", function (event) {
    if (!desktop.matches && event.target.closest("a")) {
      setExpanded(false);
      toggle.focus();
    }
  });
  if (desktop.addEventListener) desktop.addEventListener("change", syncViewport);
  syncViewport();
}());
