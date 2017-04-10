var timoutWarning = 900000; // Auto logout after 15 Mins.
var logoutUrl = 'logout'; // URL to logout page.

var warningTimer;

// Start warning timer.
function StartWarningTimer() {
    warningTimer = setTimeout(IdleTimeout, timoutWarning);
}

// Reset timers.
function ResetTimeOutTimer() {
    clearTimeout(warningTimer);
    StartWarningTimer();
}

// Logout the user.
function IdleTimeout() {
    window.location = logoutUrl;
}

$(function() {
   StartWarningTimer();
});