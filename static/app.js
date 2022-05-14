function changebackground(result){
    r = document.getElementById("OutputIdred"+ result).value;
    g = document.getElementById("OutputIdgreen" + result).value;
    b = document.getElementById("OutputIdblue" + result).value;
    document.getElementById('result'+ result).style.backgroundColor = 'rgb(' + r + ',' + g + ',' + b + ')';
                }
