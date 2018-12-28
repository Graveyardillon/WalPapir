$(function() {
  const redeem = $('.rightPointEffect');
  var condition = false;

  $('.hamburgerMenuOpenButton').click(function(){
    condition = (!condition);

    if(condition) {
      redeem.animate({
        top: '265px'
      }, 200);
    }else{
      redeem.animate({
        top: '170px'
      }, 200);
    }
  });
});
