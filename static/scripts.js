
let coll = document.getElementsByClassName('collapsible-qr-options');
let i
for (i = 0; i < coll.length; i++) {
    coll[i].addEventListener("click", function (){
        this.classList.toggle("active");
        let qr_opt = this.firstElementChild;
        let content = qr_opt.nextElementSibling;
        if (content.style.display === "block"){
            content.style.display = "none";
        }else {
            content.style.display = "block";
        }
    });
}