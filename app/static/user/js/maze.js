var canL = false,
    canR = false,
    canU = false,
    canD = false;
var m;
var tomove = new Array(24);
tomove[0] = "D",
    tomove[1] = "R",
    tomove[2] = "LR",
    tomove[3] = "DL",
    tomove[4] = "R",
    tomove[5] = "L",
    tomove[6] = "UDR",
    tomove[7] = "L",
    tomove[8] = "DR",
    tomove[9] = "UDL",
    tomove[10] = "DR",
    tomove[11] = "L",
    tomove[12] = "UD",
    tomove[13] = "DR",
    tomove[14] = "UL",
    tomove[15] = "UDM",
    tomove[16] = "UR",
    tomove[17] = "L",
    tomove[18] = "U",
    tomove[19] = "U",
    tomove[20] = "R",
    tomove[21] = "ULR",
    tomove[22] = "L",
    tomove[23] = "D"

function aa() {

    canmove();
}

function canmove() {
    renl = parseInt($('#ren').css('margin-left'));
    rent = parseInt($('#ren').css('margin-top'))
    m = renl / 80 + rent / 60 * 6;
    var ss = tomove[m];
    if (ss.indexOf("U") >= 0) {
        canU = true;
    }

    if (ss.indexOf("D") >= 0) {
        canD = true;
    }
    if (ss.indexOf("L") >= 0) {
        canL = true;
    }
    if (ss.indexOf("R") >= 0) {
        canR = true;
    }

}

function moveL() {
    if (canL) {
        if (tomove[m - 1].indexOf("M") == -1) {
            var oldL = parseInt($('#ren').css('margin-left'));
            var newL = oldL - 80;
            var change = newL + "px";
            $('#ren').css('margin-left', change);
            canL = false;
            canR = false;
            canU = false;
            canD = false;
        } else {
            $('#myModal').modal('show');
            $('#mission01').show();
        }
    }
    aa();
}

function moveR() {
    if (canR) {
        if (tomove[m + 1].indexOf("M") == -1) {
            var oldL = parseInt($('#ren').css('margin-left'));
            var newL = oldL + 80;
            var change = newL + "px";
            $('#ren').css('margin-left', change);
            canL = false;
            canR = false;
            canU = false;
            canD = false;
        } else {
            $('#myModal').modal('show');
            $('#mission01').show();
        }
    }
    aa();
}

function moveD() {
    if (canD) {
        if (tomove[m + 6].indexOf("M") == -1) {
            var oldL = parseInt($('#ren').css('margin-top'));
            var newL = oldL + 60;
            var change = newL + "px";
            $('#ren').css('margin-top', change);
            canL = false;
            canR = false;
            canU = false;
            canD = false;
        } else {
            $('#myModal').modal('show');
            $('#mission01').show();
        }
    }
    aa();
}

function moveU() {
    if (canU) {
        if (tomove[m - 6].indexOf("M") == -1) {
            var oldL = parseInt($('#ren').css('margin-top'));
            var newL = oldL - 60;
            var change = newL + "px";
            $('#ren').css('margin-top', change);
            canL = false;
            canR = false;
            canU = false;
            canD = false;
        } else {
            $('#myModal').modal('show');
            $('#mission01').show();
        }
    }
    aa();
}　
$(document).keydown(function(event) {　　　
    if (event.keyCode == 37) {
        moveL();
    }
    if (event.keyCode == 38) {　　　　　　
        moveU();　　　
    }
    if (event.keyCode == 39) {　　　　　　
        moveR();　　　
    }
    if (event.keyCode == 40) {　　　　　　
        moveD();　　　
    }　
});