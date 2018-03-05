function getCookie(name) {  
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
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

function start(str) {
    var textArea = document.createElement('textarea');
    textArea.innerHTML = str;
    return textArea.value;
}


$(document).ready(function () {
  start();
  $.get("/get-items")
      .done(function(response) {
          console.log(" see item.html")
          var textElement = $("#Post-list");
          textElement.data('max-time',response['max-time']);
          textElement.html('')
          for (var i = 0; i < response.items.length; i++) {
              item = response.items[i];
             var textArea = document.createElement('textarea');
             textArea.innerHTML = item.html;
             var new_item = textArea.value;
              textElement.append(new_item);
              getCommentList(item.id,"2018-01-01T20:26:05.433832-04:00")
          }
          $("button[id*='commentPost_']").off().click(comment);
      });

  $("#postbuttom").off().click(function(event) {
    event.preventDefault();
    var FormPost = $("#post-form").serializeArray();
    var formFocus = $("#Post-list")
    var content = {};
    $(FormPost).each(function() {
        content[this.name] = this.value;
    });
    $.post("/post-form",content)
    .done(function(response) {
        getUpdates();
    });
    $("#id_text").val(" ")
});
  var csrftoken = getCookie('csrftoken');
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  });
});


function getUpdates() {
    var textElement = $("#Post-list")
    var max_time = textElement.data("max-time")
    $.get("/get-changes/"+ max_time)
      .done(function(response) {
          textElement.data('max-time', response['max-time']);
          for (var i = 0; i < response.items.length; i++) {
             console.log("enter")
             var item = response.items[i];
             var textArea = document.createElement('textarea');
             textArea.innerHTML = item.html;
             var new_item = textArea.value;
             textElement.prepend(new_item);
             getCommentList(item.id,"2018-01-01T20:26:05.433832-04:00")
          }
          $("button[id*='commentPost_']").off().click(comment);
      });
}

function getUpdatesComment(id,max_time) {
    var textElement = $("#comment-list_"+ id)
    $.get("/get-changesComment/"+ max_time+"/"+id)
      .done(function(response) {
          textElement.data('max-time', response['max-time']);
          for (var i = 0; i < response.items.length; i++) {
             console.log("enter")
             var item = response.items[i];
             var textArea = document.createElement('textarea');
             textArea.innerHTML = item.html;
             var new_item = textArea.value;
             textElement.append(new_item);
          }
      });
}


function getCommentList(id,max_time) {
    var textElement = $("#comment-list_"+ id)
    $.get("/get-allComment/"+id)
      .done(function(response) {
          textElement.data('max-time', response['max-time']);
          for (var i = 0; i < response.items.length; i++) {
             var item = response.items[i];
             var textArea = document.createElement('textarea');
             textArea.innerHTML = item.html;
             var new_item = textArea.value;
             textElement.append(new_item);
          }
      });
}

function comment() {
  var itemField = $("#item-field_"+jQuery(this).attr("id"));
  var id_list = jQuery(this).attr("id");
  postid = jQuery(this).attr("id").replace("commentPost_", "")
  $.post("/comment-form", {"postID": postid,"text":itemField.val()})
  .done(function(response) {
    getUpdatesComment(response.postid,response.maxtime);
    $("#item-field_"+id_list).val(" ")
  });
}


 window.setInterval(getUpdates, 5000);
