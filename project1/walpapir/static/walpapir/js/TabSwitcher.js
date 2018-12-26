$(function() {
  $(".squarePostTab").click(function(){
    $(".favContent").css("display","none");
    $(".postContent").css("display", "inline");
    $(".squarePostTab").addClass("activePostTab");
    $(".squareFavTab").removeClass("activeFabTab");
  });

  $(".squareFavTab").click(function(){
    $(".favContent").css("display","inline");
    $(".postContent").css("display","none");
    $(".squarePostTab").removeClass("activePostTab");
    $(".squareFavTab").addClass("activeFabTab");
  });
})
