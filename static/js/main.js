function usunkurwe(){
    var kurwe = document.getElementById("error");
    kurwe.style.display = "none";
    var kurwe = document.getElementById("error-list");
    kurwe.innerHTML = "<li> <input type='button' value='x' onclick='usunkurwe()'> </li>";
}

function flash(message){
    console.log("sex")
    var kurwe = document.getElementById("error-list");
    kurwe.innerHTML += "<li>" + message + "</li>";
    var kurwe = document.getElementById("error");
    kurwe.style.display = "block";
}