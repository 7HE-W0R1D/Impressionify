function refresh_card(data){
    $("#diy-content-03" + " .card-image").css("background-image", "url(" + data["url"] + ")")
    $("#diy-content-03" + " .upload-title").text(data["title"])
    $("#diy-content-03" + " .upload-author").text("by " + data["year"])
    $("#diy-content-03" + " .upload-support").text(data["alt_text"])
    $("#diy-content-03" + " .mainbtn-1").attr("href", data["info_link"])
}

$(function() {

    $("#diy-content-02 .jmp-btn").on("click", function(){
        var img = $("#diy-content-01 .card-image").attr("value")
        var art = $("#diy-content-02 .jmp-btn").attr("selected_art");
        $.ajax({
			data : {"art": art, "img": img},
			type : 'POST',
			url : '/finaldisplay'
		}).done(function(data) {
            refresh_card(data["info"])
            $("#diy-content-03" + " .mainbtn-1").attr("download", "result.jpg")
        })
    });
});