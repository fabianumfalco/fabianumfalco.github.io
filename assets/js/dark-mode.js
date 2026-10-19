/* Apply the theme before styles load; no external dependencies. */
(function () {
  "use strict";
  var key = "portfolio-theme";
  var preference = "system";
  var media = window.matchMedia("(prefers-color-scheme: dark)");

  try {
    var saved = window.localStorage.getItem(key);
    if (["light", "dark", "system"].includes(saved)) {
      preference = saved;
    } else if (document.cookie.split(";").some(function (cookie) {
      return cookie.trim() === "mode=dark-mode";
    })) {
      // Preserve the previous site's explicit dark preference.
      preference = "dark";
      window.localStorage.setItem(key, preference);
    }
  } catch (_) {
    // System preference remains available if browser storage is blocked.
  }

  function apply() {
    var theme = preference === "system" ? (media.matches ? "dark" : "light") : preference;
    document.documentElement.dataset.theme = theme;
  }
  apply();

  if (media.addEventListener) media.addEventListener("change", apply);
  window.addEventListener("storage", function (event) {
    if (event.key !== key && event.key !== null) return;
    preference = ["light", "dark", "system"].includes(event.newValue) ? event.newValue : "system";
    apply();
    var control = document.getElementById("theme-preference");
    if (control) control.value = preference;
  });

  document.addEventListener("DOMContentLoaded", function () {
    var control = document.getElementById("theme-preference");
    if (!control) return;
    control.value = preference;
    control.disabled = false;
    control.addEventListener("change", function () {
      preference = control.value;
      apply();
      try {
        window.localStorage.setItem(key, preference);
        document.cookie = "mode=; Max-Age=0; Path=/; SameSite=Lax";
      } catch (_) {
        // Keep the selection for this page even when persistence is unavailable.
      }
    });
  });
}());
