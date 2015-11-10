//$(document).scroll(function(){
//    var height = $('header#header').outerHeight(true);
//    if ($(this).scrollTop() - height > -35) {
//        console.log(true);
//    } else {
//        console.log(false);
//    }
//});
var menu = {
    show: function(){
        $('#col-nav-mobile').animate({
            left: 0
        }, 500);
        $('#col-nav-mobile').click(menu.hide);
        $('#col-nav-mobile #nav').click(function(event){
            event.stopPropagation();
        });
    },
    hide: function(){
        $('#col-nav-mobile').animate({
            left: '-100%'
        }, 500);
    }
}
$('#navMobile').click(menu.show);
$(function () {
    $('[data-toggle="tooltip"]').tooltip()
});

$('.menu > dl > dt').click(function(){
    var name = $(this).data('link');
    if ($('dd.' + name).hasClass('active')) $('dd.' + name).removeClass('active');
    else $('dd.' + name).addClass('active');
    return false;
});


