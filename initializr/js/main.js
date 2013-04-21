
$(document).ready(function(){

//ADD A NOTE METHOD, Posts JSON to REST Endpoint then on success renders Handlebars Template of note on top of stack and clears note form.
var source   = "<div class='well well-small'><span class='label label-info'>{{user}}  {{time}}</span><p>{{notebody}}</p></div>";
var template = Handlebars.compile(source);
var working = false;
$('#addNoteForm').submit(function(e){
        e.preventDefault();
        console.log("Submit Button Detected");
        if(working) return false;
        working = true;
        $('#submit').val('Working..');
        $('span.error').remove();

        $.post('/comments/',$(this).serialize(),function(msg){

            working = false;
            var context = {user:window.user, notebody: msg.body};
            var html    = template(context);
            $('#notes').prepend(html);
                $('#notes div:first').hide().slideDown();
                $('#notesbody').val('');
        });
    });
//ADD A DOCUMENT METHOD
    $('#documentSelect li').click(function(e){
        e.preventDefault();
        console.log("Submit Button Detected");
        if(working) return false;
        working = true;
        $('#submit').val('Working..');
        $('span.error').remove();
        title = $(this).text();
        data = {title:title, submission_ip:"127.0.0.1", request_date: "2013-03-04"};
$.ajax({
  type: "POST",
  url: "/documents/",
  data: data,
  success: function(msg){
        alert( "Data Saved: " + msg );
        working= false;
  },
  error: function(XMLHttpRequest, textStatus, errorThrown) {
        $('#documentError').removeClass('hidden');
        $('#documentError').text(XMLHttpRequest.responseText);
        working= false;
  }
});
        $('#documents').prepend("<li class='span2'><div class='thumbnail'><img src='/static/img/unknown.png' alt=''><h4>"+title+"</h4><p>Requested on April 16, 2013, 10:51 a.m.</p><p><a href='#' target='_blank' class='btn btn-primary'><i class='icon-plus icon-white'></i>Add</a></p></div></li>");
        working= false;
    });

$('.uploadButton').click(function(e){
    docId = $(this).data('id');
$("#fileField[data-id='" + docId + "']").click();
});
});





