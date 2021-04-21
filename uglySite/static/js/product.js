var zoom_area = document.getElementById("zoom-area");
var image = document.getElementById("main-image");
var ghost = document.getElementById("ghost");
var ghostCT = ghost.getContext("2d");
var actual_main = 0;
var front = "";
var back = "";
var today = new Date();
var expirationDate = new Date().setMonth(today.getMonth()+1);
var submittable = true;



function getCookie(name) {
    // Split cookie string and get all individual name=value pairs in an array
    var cookieArr = document.cookie.split(";");
    
    // Loop through the array elements
    for(var i = 0; i < cookieArr.length; i++) {
        var cookiePair = cookieArr[i].split("=");
        
        /* Removing whitespace at the beginning of the cookie name
        and compare it with the given string */
        if(name == cookiePair[0].trim()) {
            // Decode the cookie value and return
            return decodeURIComponent(cookiePair[1]);
        }
    }
    
    // Return null if not found
    return null;
}



/*
{
    "11": {
        "src": "https//...",
        "name" "Calcetines de gatito",
        "price": "120",
        "#FF0000": "2",
        "#FFFF00": "1",
    }
    ...
}
*/

image.onmousemove = function(e){
    if(!isMObile){
        var posX = ((e.offsetX/image.offsetWidth)*100);
        var posY = ((e.offsetY/image.offsetHeight)*100);

        zoom_area.style.display = "block";
        zoom_area.style.top= (e.clientY + 30) + "px";
        zoom_area.style.left= (e.clientX + 30) + "px";
        zoom_area.style.backgroundPositionX = posX + "%";
        zoom_area.style.backgroundPositionY =  posY + "%";
    }
};

image.addEventListener('mouseleave', function(){
    zoom_area.style.display = "none";
    zoom_area.style.backgroundPosition = "center";
});


function ghostURL(ghostimg){
    ghostCT.clearRect(0,0, ghost.width, ghost.height);
    ghostCT.drawImage(document.getElementById("ghost-img"), (1000-ghostimg.width)/2, (1000-ghostimg.height)/2, ghostimg.width, ghostimg.height);
    ghostCT.drawImage(document.getElementById("main-image"), 0,0, 1000, 1000); 
    return ghost.toDataURL();
}

function zoomCanvas(cleanUrl){
    var ghostimg = document.getElementById("ghost-img");
    ghostimg.src=cleanUrl;
    ghostimg.width = 200;
    ghostimg.height = 900;
    document.getElementById("zoom-area").style.backgroundImage = "url('" + ghostURL(ghostimg) + "')";
    
    //Just in case this has not loaded
    ghostimg.onload = function(){
        document.getElementById("zoom-area").style.backgroundImage = "url('" + ghostURL(ghostimg) + "')";
    };
}


function makeMain(li, num){
    
    var old_li = document.getElementsByClassName("image-selected")[0];
    old_li.classList.remove("image-selected");
    
    var main = document.getElementById("main-image");
    var image = li.children[1];
   
    main.src = image.src;
    actual_main = num;

    
    if(customProd){
        var url = document.getElementById("img"+actual_main.toString()).style.backgroundImage; 
        var cleanUrl = url.replace('url(','').replace(')','').replace(/\"/gi, "");
        main.style.backgroundImage = url;
        zoomCanvas(cleanUrl);
    }else{
        document.getElementById("zoom-area").style.backgroundImage = "url('" + main.src + "')";
    }
    
    li.classList.add("image-selected");
}



function changeColor(event){
    var color = event.target.value;
    document.getElementById("main-image").style.backgroundColor = color;
    var secondary= document.getElementsByClassName("secondary");
    for(var index=0;index < secondary.length;index++){
        secondary[index].style.backgroundColor = color;
    }
    document.getElementById("zoom-area").style.backgroundColor = color;
}

document.getElementById("COLPICK").addEventListener("input", changeColor, false);


var descripButton = document.getElementById("description");
var reviewButton = document.getElementById("reviews");
var description = document.getElementById("D");
var reviews = document.getElementById("V");

descripButton.onclick = function(){
    descripButton.style.fontWeight = "bold";
    reviewButton.style.fontWeight = "normal";
    description.style.display="block";
    reviews.style.display="none";
};

reviewButton.onclick = function(){
    descripButton.style.fontWeight = "normal";
    reviewButton.style.fontWeight = "bold";
    description.style.display="none";
    reviews.style.display="block";
};


var star1 = document.getElementById("setStar1");
var star2 = document.getElementById("setStar2");
var star3 = document.getElementById("setStar3");
var star4 = document.getElementById("setStar4");
var star5 = document.getElementById("setStar5");
var ratingField = document.getElementById("id_rating");
var gold = "#FFC800";
var gray = "rgb(0,0,0,0.3)";

star1.onclick = function(){
    star1.style.backgroundColor=gold;
    star2.style.backgroundColor=gray;
    star3.style.backgroundColor=gray;
    star4.style.backgroundColor=gray;
    star5.style.backgroundColor=gray;
    ratingField.setAttribute("value", "1.00")
}
star2.onclick = function(){
    star1.style.backgroundColor=gold;
    star2.style.backgroundColor=gold;
    star3.style.backgroundColor=gray;
    star4.style.backgroundColor=gray;
    star5.style.backgroundColor=gray;
    ratingField.setAttribute("value", "2.00")
}
star3.onclick = function(){
    star1.style.backgroundColor=gold;
    star2.style.backgroundColor=gold;
    star3.style.backgroundColor=gold;
    star4.style.backgroundColor=gray;
    star5.style.backgroundColor=gray;
    ratingField.setAttribute("value", "3.00")
}
star4.onclick = function(){
    star1.style.backgroundColor=gold;
    star2.style.backgroundColor=gold;
    star3.style.backgroundColor=gold;
    star4.style.backgroundColor=gold;
    star5.style.backgroundColor=gray;
    ratingField.setAttribute("value", "4.00")
}
star5.onclick = function(){
    star1.style.backgroundColor=gold;
    star2.style.backgroundColor=gold;
    star3.style.backgroundColor=gold;
    star4.style.backgroundColor=gold;
    star5.style.backgroundColor=gold;
    ratingField.setAttribute("value", "5.00")
}

var input = document.getElementById("cartQuantity");

document.getElementById("qMore").onclick = function(){
    var value = parseInt(input.getAttribute("value"));
    input.setAttribute("value",(value+1).toString());
    input.value = (value+1);
}

document.getElementById("qLess").onclick = function(){
    var value = parseInt(input.getAttribute("value"));
    
    if(value>=2){
        input.setAttribute("value",(value-1).toString());
        input.value = (value-1);
    }else if (value<=0){
        alert("Error! Valor igual o menor a cero!");
    }
}

input.addEventListener('input', function(e){
    input.setAttribute("value",e.target.value.toString());
    input.value = e.target.value;
});


var cartButton = document.getElementById("addtocart");

cartButton.onclick = function(){
    
    var color = document.getElementById("COLPICK").value;
    var quantity = document.getElementById("cartQuantity").value;

    if ((!(parseInt(quantity)<0)) && ((customProd!="True")||((customProd=="True")&&(submittable==true)))){
        if(customProd=="True"){
            if (front!=""||back!=""){
                if (cart[prodNum] == null){
                    cart[prodNum] = {
                        "src": document.getElementById("img0").getAttribute("src"),
                        "name": prodName,
                        "price": prodPrice,
                        "custom": customProd,
                        "variations": {},
                    };
                    var src = "";
                    if(front!=""){src = front;}
                    cart[prodNum]["variations"][uuid] = {/*"src": src,*/};
                    cart[prodNum]["variations"][uuid][color] = quantity;
                } else if (cart[prodNum]["variations"][uuid] == null){
                    var src = "";
                    if(front!=""){src = front;}
                    cart[prodNum]["variations"][uuid] = {/*"src": src,*/};  //src loading takes too much time
                    cart[prodNum]["variations"][uuid][color] = quantity;
                }else if (cart[prodNum]["variations"][uuid][color] == null){
                    cart[prodNum]["variations"][uuid][color] = quantity;
                }else{
                    cart[prodNum]["variations"][uuid][color] = (parseInt(cart[prodNum]["variations"][uuid][color]) + parseInt(quantity)).toString();
                }
            }else{
                alert("No has agregado ninguna imagen!");
            }
        }else{
            if (cart[prodNum] == null){
                cart[prodNum] = {
                    "src": document.getElementById("img0").getAttribute("src"),
                    "name": prodName,
                    "price": prodPrice,
                    "custom": customProd,
                };
                cart[prodNum][color] = quantity;
            } else if (cart[prodNum][color] == null){
                cart[prodNum][color] = quantity;
            }else{
                cart[prodNum][color] = (parseInt(cart[prodNum][color]) + parseInt(quantity)).toString();
            }
        }
        
        localStorage.setItem("cart", JSON.stringify(cart));
    
        if(customProd!="True"||(customProd=="True"&&(front!=""||back!=""))){
            var totalInCart = localStorage.getItem("totalInCart");
            if(totalInCart == null){
                totalInCart = "0";
            }
            totalInCart = (parseInt(totalInCart) + parseInt(quantity)).toString();
            localStorage.setItem("totalInCart", totalInCart.toString());
        
            var totalPrice = localStorage.getItem("totalPrice");
            if(totalPrice == null){
                totalPrice = "0";
            }
            totalPrice = (parseFloat(totalPrice) + (parseFloat(quantity)*parseFloat(prodPrice))).toString();
            localStorage.setItem("totalPrice", totalPrice.toString());
        
            var miniTotal = document.getElementById("miniCartTotal");
            miniTotal.style.display = "block";
            miniTotal.innerText = totalInCart;
        
            UpdateMini();
        }
    }else if(customProd=="True" && submittable==false){
        alert("Espera un poco! La imagen se está subiendo.");
    }
};


function submitAndChange (){
    $.ajax({
        type:'POST',
        url: page_url,
        data:
        {
            addToCart:$("#cartQuantity").val(),
            uuid: new_uuid,
            fronturl: front,
            backurl: back,
            color: $('#COLPICK').val(),
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
        },
        success:function(json){
            if(json["success"] == "True"){
                uuid = json["uuid"];
                new_uuid = json["newuuid"];
                urls[json["uuid"]] = json["fronturl"];
                localStorage.setItem("imagesURLS",  JSON.stringify(urls));
                submittable = true;
            }else{
                alert(json["errorMsg"]);
            }
        }
    })
}

$(document).on('submit','#imagesForm',function(e){
    e.preventDefault();
    submitAndChange();
});

function ghostUploadURL(url, face){
    var ghostimg = document.getElementById("ghost-img-"+face);
    var ghostCan = document.getElementById("ghost-"+face);
    var ctxt = ghostCan.getContext("2d");
    var returnurl;

    ghostimg.src = url;
    ghostimg.width=1000;
    ghostimg.height=4500;

    ghostimg.onload = function(){
        ctxt.clearRect(0,0, ghostCan.width, ghostCan.height);
        ctxt.drawImage(document.getElementById("ghost-img"), (1000-ghostimg.width)/2, (4500-ghostimg.height)/2, ghostimg.width, ghostimg.height);
        returnurl = ghostCan.toDataURL();
        if(face=="front"){front=returnurl;}else if(face=="back"){back=returnurl;}
        submitAndChange();
    }
}


function loadFront(event){
    submittable = false;
    var cleanUrl = URL.createObjectURL(event.target.files[0]);
    var url = "url("+cleanUrl+")";
    document.getElementById("img0").style.backgroundImage = url;

    if(actual_main==0){
        document.getElementById("main-image").style.backgroundImage = url;
        zoomCanvas(cleanUrl);
    }
    ghostUploadURL(cleanUrl, "front");
}

function loadBack(event){
    submittable = false;
    var cleanUrl = URL.createObjectURL(event.target.files[0]);
    var url = "url("+cleanUrl+")";
    document.getElementById("img1").style.backgroundImage = url;

    if(actual_main==1){
        document.getElementById("main-image").style.backgroundImage = url;
        zoomCanvas(cleanUrl);
    }

    ghostUploadURL(cleanUrl, "back");
}

