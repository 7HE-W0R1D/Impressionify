function scroll_lucky(btn_id, pgid = "#lucky-content"){

    var gap = 32;
    var btn_val = btn_id;
    // alert(btn_val);
    var combo_row = $(pgid + " .combo-row");
    var currpg = combo_row.attr("currpg");
    var maxpg = $(pgid + " .combo-row .mdc-card").length - 1;
    // alert(maxpg);
    var currwidth = ($(pgid + " .combo-row .mdc-card").width() + 2); //preserve the right edge
    // alert(currwidth);
    var currtrans = (-1) * currpg * (currwidth + gap);
    // alert(currtrans);
    var transformdist = currwidth + gap;
    if (btn_val == "nxt-itm") {
        //scroll translatex -
        transformdist = -transformdist;
        if(currpg < maxpg) {
            //not the last pange
            transformdist += currtrans;
            run(combo_row, [{y:currtrans}, {y:transformdist}]);

            if (currpg == 0) {
                $(pgid + " ." + "prv-itm").removeAttr("disabled");
            }
            else if (currpg == maxpg - 1) {
                //last page
                $(pgid + " ." + btn_val).attr("disabled", "");
            }
            currpg ++;
            combo_row.attr("currpg", currpg);
        }
    }
    else {
        if (currpg > 0) {
            if (currpg == maxpg) {
                $(pgid + " ." + "nxt-itm").removeAttr("disabled");
            }
            else if (currpg == 1) {
                //approaching first pg
                $(pgid + " ." + btn_val).attr("disabled", "");
            }

            transformdist += currtrans;
            // alert(transformdist);
            run(combo_row, [{y:currtrans}, {y:transformdist}]);
            currpg --;
            combo_row.attr("currpg", currpg);
        }
    }
}


function run(element, v){
    // Thanks https://stackoverflow.com/questions/49555672/translatex-using-jquery for saving my sleep
    $(v[0]).animate(v[1], {
        duration: 500,
        step: function(val) {
            //Adding the transform to your element
            element.css("transform", `translateX(${val}px)`); 
        }
    })
}