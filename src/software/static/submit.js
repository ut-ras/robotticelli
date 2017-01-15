function updateOutputDisplay(response) {
}

$(document).ready(function() {
  $('#primavera-form').submit(function(e) {
    e.preventDefault();
    myform = new FormData($('#primavera-form')[0]);
    $.ajax({
        url:'/submit',
        type:'POST',
        data: myform,
        processData: false,
        contentType: false,
        //async: false,
        cache: false,
        success:function(response) {
          $("#output").attr('src', response.img)
          console.log("success")
          console.log(response.img)
        },
    });
    console.log("pressed");
  });
})
