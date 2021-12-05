function replace_cards(data) {
    var img_lst = data["info"]
    $.each(img_lst, function(index, value) {
        $("#diy-img-" + index + " .select-art").attr("value", value["url"])
        $("#diy-img-" + index + " .card-image").css("background-image", "url(" + value["url"] + ")")
        $("#diy-img-" + index + " .upload-title").text(value["title"])
        $("#diy-img-" + index + " .upload-author").text("by " + value["year"])
        $("#diy-img-" + index + " .upload-support").text(value["alt_text"])
        $("#diy-img-" + index + " .mainbtn-1").attr("href", value["info_link"])
      });
}

function refresh_queue(data) {
    $("#diy-content-02").fadeOut(200)
    setTimeout(
        function() 
        {
            var combo_row = $("#diy-content-02 .combo-row")
            combo_row.attr("currpg", 0)
            combo_row.css("transform", "translateX(0px)")
            replace_cards(data)
        }, 250);
    $("#diy-content-02 .prv-itm").attr("disabled", "")
    $("#diy-content-02 .nxt-itm").removeAttr("disabled")
    $("#diy-content-02").fadeIn(200)
    return false
}

$(function() {

    $('#diy-content-02 .select-art').on('click', function(e){
        //selected an art
        var selected_url = $(this).attr("value");
        var fab_btn = $("#diy-content-02 .jmp-btn");
        fab_btn.attr("selected_art", selected_url);
        fab_btn.addClass("mdc-fab--exited")
        setTimeout(
            function() 
            {
                $("#diy-content-02 .jmp-btn .material-icons").text("done");
                fab_btn.removeClass("mdc-fab--exited")
            }, 500);
    });

    $('#jmp-diy-fab').on('click', function(){
        var keywords = $("#refresh-queue").attr("keyword")
        $(".select-art").attr("disabled", "");
		$.ajax({
			data : {"num": 5, "keyword": keywords},
			type : 'POST',
			url : '/getrandart'
		}).done(function(data) {
			replace_cards(data)
            $(".select-art").removeAttr("disabled");
        })
	});

    $('#refresh-queue').on('click', function(){
        var keywords = $("#refresh-queue").attr("keyword")
        $(".select-art").attr("disabled", "");
		$.ajax({
			data : {"num": 5, "keyword": keywords},
			type : 'POST',
			url : '/getrandart'
		}).done(function(data) {
            refresh_queue(data);
            $(".select-art").removeAttr("disabled");
        })
	});

    $("#search-queue").on("click", function(){
        var keyword = "[\"" + $("#diy-search").val() + "\"]"
        $(".select-art").attr("disabled", "");
        $.ajax({
			data : {"num": 5, "keyword": keyword},
			type : 'POST',
			url : '/getsearchart'
		}).done(function(data) {
            refresh_queue(data)
            $(".select-art").removeAttr("disabled");
        })
    });

    $('#diy-search').on("keyup", function (e) {
        if (e.which == 13) {
            var keyword = "[\"" + $("#diy-search").val() + "\"]"
            $(".select-art").attr("disabled", "");
            $.ajax({
                data : {"num": 5, "keyword": keyword},
                type : 'POST',
                url : '/getsearchart'
            }).done(function(data) {
                refresh_queue(data)
                $(".select-art").removeAttr("disabled");
            })
        }
      });


});



function showsearch() {
	var searchbar = document.getElementById("search-bar");
	if (window.getComputedStyle(searchbar).display === "none") {
        $("#diy-content-02 card-dyna").addClass("card-normal__dyna")
        $("#diy-content-02 card-dyna").addClass("card-normal__dyna")
		$("#search-bar").fadeIn(300);
	}
	else {
        $("#diy-content-02 card-dyna").removeClass("card-normal__dyna")
        $("#diy-content-02 card-dyna").removeClass("card-normal__dyna")
		$("#search-bar").fadeOut(300);
	}
}