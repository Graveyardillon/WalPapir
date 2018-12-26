$(function() {
  var nav = $('.menu');
  offset = nav.offset();

  $('head').append(
    '<style>#wrap{display:none;}'
  );
  $(window).on("load", function() {
    $('#wrap').delay(50).fadeIn("slow");
  });

  $(window).scroll(function () {
    if($(window).scrollTop() > offset.top) {
      nav.addClass("fixedPosition");
    } else {
      nav.removeClass("fixedPosition");
    }
  });
});

//This source code contains an action of fading in
