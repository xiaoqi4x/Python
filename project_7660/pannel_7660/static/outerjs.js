var h = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;
var h1 = h - 970;
document.getElementById("mdiv").setAttribute("style","height: " + h1 + "px");
var nodes = document.querySelectorAll(".td_font");
for (i=0;i<nodes.length;i++){
    var value = document.querySelectorAll(".td_font")[i].innerHTML;
    if ( value == "SIM1" || value == "SIM0" || value == "ABORTED" || value == "CAMPAIGN_INCOMPLETE" || value ==
        "PENDING" || value == "SYNC_ERROR" || value == "PC_DOWN" || value == "DONE" || value == "false" || value == "OFF"){
        document.querySelectorAll(".td_font")[i].style.color = "red";
    }
}
var nodes = document.querySelectorAll(".td_font_1");
for (i=0;i<nodes.length;i++){
    var value = document.querySelectorAll(".td_font_1")[i].innerHTML;
    if ( value == "true" || value == "SIM1" || value == "SIM0" ){
        document.querySelectorAll(".td_font_1")[i].style.color = "red";
    }
}
var nodes = document.querySelectorAll(".td_section");
for (i=0;i<nodes.length;i++){
    var value = document.querySelectorAll(".td_section")[i].innerHTML;
    if ( value == "Track-1" || value == "Track-3" || value == "MK5"){
       document.querySelectorAll(".td_section")[i].style.color = "red";
    }
}
/*function section_info_on(x){
    x.style.backgroundColor = "red"
}
function section_info_leave(x){
    x.style.backgroundColor = "red"
}*/









