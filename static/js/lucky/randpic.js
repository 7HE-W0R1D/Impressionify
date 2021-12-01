$(function() {

	$('#lucky-refresh').on('click', function(e){
        //refresh content with new things
		$.ajax({
			type: 'POST',
			url: '/refreshlucky',
		}).done(function(data) {
			$("#lucky-content").fadeOut(200)
			setTimeout(
				function() 
				{
					var combo_row = $("#lucky-content .combo-row")
					combo_row.attr("currpg", 0)
					combo_row.css("transform", "translateX(0px)")
					$("#lucky-art .card-image").css("background-image", "url(" + data["info"]["art"]["url"] + ")")
					$("#lucky-art .upload-title").text(data["info"]["art"]["title"])
					$("#lucky-art .upload-author").text("by " + data["info"]["art"]["year"])
					$("#lucky-art .upload-support").text(data["info"]["art"]["alt_text"])
					$("#lucky-art .mainbtn-1").attr("href", data["info"]["art"]["info_link"])
		
					$("#lucky-unsplash .card-image").css("background-image", "url(" + data["info"]["unsplash"]["url"] + ")")
					$("#lucky-unsplash .upload-title").text(data["info"]["unsplash"]["title"])
					$("#lucky-unsplash .upload-author").text("by " + data["info"]["unsplash"]["year"])
					$("#lucky-unsplash .upload-support").text(data["info"]["unsplash"]["alt_text"])
					$("#lucky-unsplash .mainbtn-1").attr("href", data["info"]["unsplash"]["info_link"])
		
					$("#lucky-deepai .card-image").css("background-image", "url(" + data["info"]["deepai"]["url"] + ")")
					$("#lucky-deepai .upload-title").text(data["info"]["deepai"]["title"])
					$("#lucky-deepai .upload-author").text("by " + data["info"]["deepai"]["year"])
					$("#lucky-deepai .upload-support").text(data["info"]["deepai"]["alt_text"])
					$("#lucky-deepai .mainbtn-1").attr("href", data["info"]["deepai"]["info_link"])
				}, 250);

			$("#lucky-content .prv-itm").attr("disabled", "")
			$("#lucky-content .nxt-itm").removeAttr("disabled")
			$("#lucky-content").fadeIn(200)
		})
    });

	$(document)
	  .ajaxStart(function () {
		linearProgress.open();
	  })
	  .ajaxStop(function () {
		linearProgress.close();
	  });

});