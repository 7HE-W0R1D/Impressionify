var ripple = '<span class="mdc-list-item__ripple sidebar"></span>'

$(function() {

    $('.side-bar-btn').on('click', function(e){
		var curr_tab = $(".mdc-list-item--activated");
		var tgt_tab = $(this);
		var pagenum = 0;
		var attr = $(this).attr('page');
		if (typeof attr !== typeof undefined && attr !== false) {
			pagenum = attr;
		}

		if (curr_tab.attr("href") != tgt_tab.attr('href')) {
			//new tab, switch
			tgt_tab.prepend(ripple);
			tgt_tab.addClass("mdc-list-item--activated");
			curr_tab.removeClass("mdc-list-item--activated");
			curr_tab.find(".mdc-list-item__ripple").remove();
		}

		$.ajax({
			data: {
				"target" : $(this).attr('href')
			},
			type: 'POST',
			url: '/switchtab',
		}).done(function(data) {
			console.log(data)
			$("#content-title").text(data["info"]["title"])
			$(".content-divider").fadeOut(200)
			$("#" + data["info"]["content_id"][pagenum]).delay(200).fadeIn(200)
			setTimeout(check_uploaded, 1500)
		})
    });

	$('.jmp-btn').on('click', function(e){
		var curr_tab = $(".mdc-list-item--activated");
		var pagenum = 0;
		var attr = $(this).attr('page');
		var tgt_tab_id = $(this).attr('href');
		var tgt_tab = $(tgt_tab_id)

		if (typeof attr !== typeof undefined && attr !== false) {
			pagenum = attr;
		}

		if (curr_tab.attr("href") != tgt_tab.attr('href')) {
			//new tab, switch ripple
			tgt_tab.prepend(ripple);
			tgt_tab.addClass("mdc-list-item--activated");
			curr_tab.removeClass("mdc-list-item--activated");
			curr_tab.find(".mdc-list-item__ripple").remove()
		}

		$.ajax({
			data: {
				"target" : $(this).attr('href')
			},
			type: 'POST',
			url: '/switchtab',
		}).done(function(data) {
			console.log(data)
			var fab_btn = $("#"+ data["info"]["content_id"][pagenum - 1] + " .jmp-btn")
			fab_btn.addClass("mdc-fab--exited")
			$("#content-title").text(data["info"]["title"])
			$(".content-divider").delay(400).fadeOut(100)
			$("#" + data["info"]["content_id"][pagenum]).delay(500).fadeIn(100)
			setTimeout(check_uploaded, 1500)
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

function check_uploaded (page_id = "diy-content-01") {
	var tgpage = document.getElementById(page_id);
	if (window.getComputedStyle(tgpage).display !== "none") {
		var img_title = $("#" + page_id + " #upload-title");
		if (img_title.text() != 'Upload Your Image!') {
			show_snack_with_nobtn("Using Previous Upload")
			$("#diy-content-01 #jmp-diy-fab").delay(800).removeClass("mdc-fab--exited")
		}
	}

}