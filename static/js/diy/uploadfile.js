$(function() {

    $('#upload_file').on('change', function(){
		var form = $('#upload_from')[0]
		var fd = new FormData(form)
		$.ajax({
			type : 'POST',
			url : '/uploadfile',
			data: fd,
			contentType: false,
			cache: false,
			processData: false,
			success:
				function(data) {
					$("#diy-content-01 .card-image").attr("value", data["org_fileloc"])
					$("#diy-content-01 .card-image").css("background-image", "url('" + data["org_fileloc"] + "')").fadeIn()
					$("#diy-content-01 .card-image").attr("img_loc", data["org_fileloc"])
					$("#diy-content-01 #upload-title").text(data["filename"])
					show_snack_with_nobtn("Successfully Uploaded")
					$("#diy-content-01 #jmp-diy-fab").delay(800).removeClass("mdc-fab--exited")
				},
			error:
				function(data) {
					show_snack_with_nobtn("Error Uploading Photo")
				},
		})
    });

	var $loading = $('#loadingDiv').hide();
	$(document)
	  .ajaxStart(function () {
		$loading.show();
	  })
	  .ajaxStop(function () {
		$loading.hide();
	  });

});