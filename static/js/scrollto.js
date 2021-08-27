// From: https://stackoverflow.com/questions/6677035/jquery-scroll-to-element
$("#scroll-down").click(function() {
    // scrollDownTo is a variable from index.html
    var offset = scrollDownTo == "#sidebar" ? 15 : 0;
    $([document.documentElement, document.body]).animate({
        scrollTop: $(scrollDownTo).offset().top + offset
    }, 700);
});

// From: https://www.w3schools.com/howto/tryit.asp?filename=tryhow_js_scroll_to_top
//Get the button
var upButton = document.getElementById("scroll-up");

// When the user scrolls down from the top of the document, show the button
window.onscroll = function() {scrollFunction()};

function scrollFunction() {
    var limit =  $("#twitter-feed").offset().top + 100;
    if (document.body.scrollTop >  limit || document.documentElement.scrollTop > limit) {
        upButton.style.display = "block";
    } else {
        upButton.style.display = "none";
    }
}

$("#scroll-up").click(function() {
    $([document.documentElement, document.body]).animate({
        scrollTop: 0
    }, 700);
});