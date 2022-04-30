
function dynamicTextQR(value){
    if (value.length === 0) {
        return;
    } else {
        let xmlhttp = new XMLHttpRequest();
        xmlhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                document.getElementById("qr-code").src = this.respnseText;
            }
        };
        xmlhttp.open("GET", "/text/?value=" + value, true);
        xmlhttp.send();
        }
    }