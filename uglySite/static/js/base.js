var miniTotal = document.getElementById("miniCartTotal");

if(localStorage.getItem("totalInCart")==null || localStorage.getItem("totalInCart")=="0"){
    miniTotal.style.display = "none";
}else{
    miniTotal.style.display = "block";
    miniTotal.innerText = localStorage.getItem("totalInCart");
}

var cartIcon = document.getElementById("cartIcon");
var miniCart = document.getElementById("miniCart");
var miniCartWidth = document.getElementById("miniCart").clientWidth;
miniCart.style.display="none";
var isMobile = screen.width<=720;
var canDisappear = false;

var urls = JSON.parse(localStorage.getItem("imagesURLS"));
if (urls==null) {
    urls = {};
}

window.addEventListener('click', function(e){
    if(!this.document.getElementById("miniCart").contains(e.target) || this.document.getElementById("miniCloser").contains(e.target)){
        this.document.getElementById("miniCart").style.display = "none";
        this.document.getElementById("miniCartFilter").style.display = "none";
    }
    if(this.document.getElementById("cartIcon").contains(e.target)){
        this.document.getElementById("miniCart").style.display = "block";
        this.document.getElementById("miniCartFilter").style.display = "block";

        gsap.from('#miniCart', {
            duration: 0.5,
            x: miniCartWidth,
            ease: "power2"
        });
        gsap.from('#miniCartFilter',{
            duration: 0.5,
            opacity: 0
        })
    }    
});

function addLine(ul, num, src, col, prodname, quantity, prodprice, custom, uuid, fronturl){
    var a = document.createElement("a");
    a.setAttribute("href", "/product"+num+"/");

    var img = document.createElement("img");
    img.setAttribute("src", src);
    img.setAttribute("class", "miniImg");
    img.style.backgroundColor = col;
    if(custom == "True"){
        img.style.backgroundImage = "url('" + fronturl + "')";
        img.style.backgroundSize = "21% 91%";
        img.style.backgroundPosition = "center";
    }

    var name = document.createElement("div");
    name.innerHTML =  quantity + "  x  " + "<span>" + prodname + "</span>" + " (" + col + ")";
    name.setAttribute("class", "miniMain");

    var price = document.createElement("div");
    price.innerText = quantity + "  x  $" + prodprice + " = $" + (parseFloat(quantity)*parseFloat(prodprice)).toString();

    var cont = document.createElement("div");
    cont.setAttribute("class", "miniCont");
    cont.appendChild(name);
    cont.appendChild(price);

    var remove = document.createElement("img");
    remove.setAttribute("src", "/static/images/remove.svg")
    remove.setAttribute("class", "miniRemove");
    if(custom=="True"){
        remove.setAttribute("onClick", "removeCustom({'num': '"+num+"', 'col': '"+col+"', 'uuid': '"+uuid+"'})");
    }else{
        remove.setAttribute("onClick", "remove({'num': '"+num+"', 'col': '"+col+"'})");
    }

    var helper = document.createElement("span");
    helper.setAttribute("class", "helper");

    var li = document.createElement("li");
    a.appendChild(helper);
    a.appendChild(img);
    a.appendChild(cont);
    a.appendChild(remove);

    li.appendChild(a);
    ul.appendChild(li);

}

const Http = new XMLHttpRequest();
const url = "/loadCustom/";


var cart = JSON.parse(localStorage.getItem("cart"));
var today = new Date();
var expirationDate = new Date();
expirationDate.setMonth(today.getMonth()+1);


function UpdateMini (){
    cart = JSON.parse(localStorage.getItem("cart"));
    if (cart==null) {
        cart = {};
        localStorage.setItem("cart", JSON.stringify(cart));
    }

    urls = JSON.parse(localStorage.getItem("imagesURLS"));
    if(urls==null){
        urls={};
    }

    if(window.location.pathname != "/checkout/"){
        console.log("JUST HERE");
        document.cookie ="cart="+JSON.stringify(cart)+"; expires="+ expirationDate +"; path=/checkout/";
    }
    
    var ul = document.getElementById("miniUl");
    ul.innerHTML = "";
    for(var num in cart){
        var price = cart[num]["price"];
        var name = cart[num]["name"];
        var src = cart[num]["src"];
        var custom = cart[num]["custom"];

        if(custom != "True"){
            console.log("HEY")
            for (var col in cart[num]){
                if(col!="src"&&col!="name"&&col!="price"&&col!="isCustom"&&col!="fronturl"&&col!="backurl"&&col!="customID"){
                    var quantity = cart[num][col];
                    addLine(ul, num, src, col, name, quantity, price, custom, "", "");
                }
            }
        }else{
            for (var variation in cart[num]["variations"]){
                var fronturl = "/media/uploads/custom/"+variation+".png";
                for (var col in cart[num]["variations"][variation]){
                    if(col!="src"){
                        var quantity = cart[num]["variations"][variation][col];
                        addLine(ul, num, src, col, name, quantity, price, custom, variation, fronturl);
                    }
                }
            }
        }
    }

    var totalPrice = localStorage.getItem("totalPrice");
    if(totalPrice == null){
        totalPrice = "0";
    }
    document.getElementById("miniTotal").innerText = "Total: $" + totalPrice;
}

function remove(json){
    var cart = JSON.parse(localStorage.getItem("cart"));
    if (cart==null) {cart = {};localStorage.setItem("cart", JSON.stringify(cart))}
    var totalPrice = localStorage.getItem("totalPrice");
    if(totalPrice == null){totalPrice = "0";}
    var totalInCart = localStorage.getItem("totalInCart");
    if(totalInCart == null){totalInCart = "0";}

    var num = json["num"];
    var col = json["col"];

    totalInCart = (parseFloat(totalInCart)-parseFloat(cart[num][col])).toString();
    totalPrice = (parseFloat(totalPrice)-(parseFloat(cart[num][col])*parseFloat(cart[num]["price"]))).toString();

    delete cart[num][col];

    localStorage.setItem("cart", JSON.stringify(cart));
    localStorage.setItem("totalInCart", totalInCart.toString());
    localStorage.setItem("totalPrice", totalPrice.toString());
    UpdateMini();
}

function removeCustom(json){
    var cart = JSON.parse(localStorage.getItem("cart"));
    if (cart==null) {cart = {};localStorage.setItem("cart", JSON.stringify(cart))}
    var totalPrice = localStorage.getItem("totalPrice");
    if(totalPrice == null){totalPrice = "0";}
    var totalInCart = localStorage.getItem("totalInCart");
    if(totalInCart == null){totalInCart = "0";}

    var num=json["num"];
    var uuid=json["uuid"];
    var col=json["col"];

    totalInCart = (parseFloat(totalInCart)-parseFloat(cart[num]["variations"][uuid][col])).toString();
    totalPrice = (parseFloat(totalPrice)-(parseFloat(cart[num]["variations"][uuid][col])*parseFloat(cart[num]["price"]))).toString();

    delete cart[num]["variations"][uuid][col];

    localStorage.setItem("cart", JSON.stringify(cart));
    localStorage.setItem("totalInCart", totalInCart.toString());
    localStorage.setItem("totalPrice", totalPrice.toString());
    UpdateMini();
}

document.getElementById("toCheckout").onclick = function(){
    window.location = "/checkout/";
};

UpdateMini();


document.getElementById("fake-footer").style.height = document.getElementById("real-footer").clientHeight+"px";