// trigger tooltips
var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl)
})

$(document).ready(function () {

    if ($(window).width() < 800) {
        $('.navbar').addClass('opaque shadow-sm');
    }
    if ($(this).scrollTop() > 7) {
        $('.navbar').addClass('opaque shadow-sm');
    }
    $(window).scroll(function () {
        if ($(this).scrollTop() > 7) {
            $('.navbar').addClass('opaque shadow-sm');
        } else if ($(this).scrollTop() <= 7) {
            if ($(window).width() < 800) {
                $('.navbar').removeClass('opaque shadow-sm');
            } else {
                $('.navbar').removeClass('opaque shadow-sm');
            }
        }
    });
    $(window).resize(function () {
        if ($(window).width() < 800) {
            $('.navbar').addClass('opaque shadow-sm');
        } else {
            $('.navbar').removeClass('opaque shadow-sm');
        }
    });

});
