
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            // Send the token to same-origin, relative URLs only.
            // Send the token only if the method warrants CSRF protection
            // Using the CSRFToken value acquired earlier
            csrftoken = getCookie('csrftoken');
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

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
        data = {title:title, project: window.project,submission_ip:"127.0.0.1"};
$.ajax({
  type: "POST",
  url: "/documents/",
  data: data,
  success: function(msg){
        working= false;
        date = "March 21 2012 11:32 am";
        $('#documents').prepend("<li class='span2'><div class='thumbnail'><img src='/static/img/unknown.png' alt=''><h4>"+title+"</h4><p>This document has just been requested.</p><form method='post' enctype='multipart/form-data' action='/documents/"+msg.id +"/'><input type='file' name='docfile' class='hidden fileField' data-id="+msg.id+" /><button class='btn uploadButton' type='button' data-id="+msg.id+">Add File</button><input type='submit' class='btn btn-primary' name='submit' value='Upload' /></form></div></li>");

  },
  error: function(XMLHttpRequest, textStatus, errorThrown) {
        $('#documentError').removeClass('hidden');
        $('#documentError').text(XMLHttpRequest.responseText);
        working= false;
  }
});
        working= false;
    });

$('.uploadButton').on('click',function(e){
    docId = $(this).data('id');
$(".fileField[data-id='" + docId + "']").click();
});

$(".pop-over").popover({animation: true,html:true,placement:"bottom"});
});





