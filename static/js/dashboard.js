document.addEventListener('DOMContentLoaded', function() {
    setTimeout(function() {
        var msgElement = document.getElementById('msg');
        if (msgElement) {
            msgElement.remove();
        }
    }, 2000); // Remove the message after 2 seconds
});
