$(function() {
  const nav = $('.menu');
  offset = nav.offset();

  $('head').append(
    '<style>#wrap{display:none;}'
  );


  $(window).scroll(function () {
    if($(window).scrollTop() > offset.top) {
      nav.addClass("fixedPosition");
    } else {
      nav.removeClass("fixedPosition");
    }
  });
});

$(window).on("load", function() {
  $('#wrap').delay(50).fadeIn("slow");
});

//This source code contains an action of fading in
