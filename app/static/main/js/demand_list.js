/**
 * Created by Kejing Lin on 2018/3/8.
 */
function clickchange(obj) {

    if ((obj.style.color) == "black") {
        $(obj).children().removeClass('glyphicon glyphicon-star-empty');
        $(obj).children().addClass('glyphicon glyphicon-star');
        obj.style.color = "#3399ff";
    }
    else {
        $(obj).children().removeClass('glyphicon glyphicon-star');
        $(obj).children().addClass('glyphicon glyphicon-star-empty');
        obj.style.color = "black";
    }
}