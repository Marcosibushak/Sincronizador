$('.button-collapse').sideNav({
      menuWidth: 300, //tamaño
      edge: 'right', //lado en que aparece
      closeOnClick: true, //se cierra al click en <a>
      draggable: true, //touch screen
    }
  );

  $(document).ready(function(){
    // the "href" attribute of the modal trigger must specify the modal ID that wants to be triggered
    $('.modal').modal();
    $("#forgot-btn").addClass("disabled");
  });

    $("#email2").on('change',function(){
      $("#forgot-btn").addClass("disabled");
      //alert($("#email2").attr("class"))
      if ($("#email2").attr("class")=="validate valid" ) {
        $("#forgot-btn").removeClass("disabled");
      }else{
        $("#forgot-btn").addClass("disabled");
      }
});

$( "#modal2" ).mousemove(function( event ) {
  $("#forgot-btn").addClass("disabled");
  //alert($("#email2").attr("class"))
  if ($("#email2").attr("class")=="validate valid" ) {
    $("#forgot-btn").removeClass("disabled");
  }else{
    $("#forgot-btn").addClass("disabled");
  }
});
