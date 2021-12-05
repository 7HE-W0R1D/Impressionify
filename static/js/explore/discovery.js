$(function() {
	$('.discover_jmp').on('click', function(e){
		var art_id = $(this).attr("value"); // stored in local dataset
         
        
		$.ajax({
			data: {
				"target" : art_id
			},
			type: 'POST',
			url: '/discover',
		}).done(function(data) {
			console.log(data)
			$("#discover-art .card-image").css("background-image", "url(" + data["info"]["art"]["url"] + ")")
			$("#discover-art .upload-title").text(data["info"]["art"]["title"])
			$("#discover-art .upload-author").text("by " + data["info"]["art"]["year"])
			$("#discover-art .upload-support").text(data["info"]["art"]["alt_text"])
			$("#discover-art .mainbtn-1").attr("href", data["info"]["art"]["info_link"])

			$("#discover-unsplash .card-image").css("background-image", "url(" + data["info"]["unsplash"]["url"] + ")")
			$("#discover-unsplash .upload-title").text(data["info"]["unsplash"]["title"])
			$("#discover-unsplash .upload-author").text("by " + data["info"]["unsplash"]["year"])
			$("#discover-unsplash .upload-support").text(data["info"]["unsplash"]["alt_text"])
			$("#discover-unsplash .mainbtn-1").attr("href", data["info"]["unsplash"]["info_link"])

			$("#discover-deepai .card-image").css("background-image", "url('/static/img/gallery/" + data["from"] +"/output.png')")

			$(".content-divider").delay(400).fadeOut(100)
			$("#explore-content-discovery").delay(500).fadeIn(100)
			$("#discover-back").delay(600).removeClass("mdc-fab--exited")
		})
    });

    $("#discover-back").on("click", function(e){
        $("#discover-back").addClass("mdc-fab--exited")
        $(".content-divider").delay(400).fadeOut(100)
        $("#explore-content").delay(500).fadeIn(100)
    });

	$(document)
	  .ajaxStart(function () {
		linearProgress.open();
	  })
	  .ajaxStop(function () {
		linearProgress.close();
	  });

});