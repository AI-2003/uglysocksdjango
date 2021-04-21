var checkBox = document.getElementById("extraCheckbox");
var secondAddress = document.getElementById("secondAddressTable");
var secondAddressHeight = secondAddress.clientHeight;
var form1 = document.getElementsByClassName("form1");
for(var index=0;index < form1.length;index++){
  form1[index].removeAttribute("required");
}
secondAddress.style.height="0px";

checkBox.onclick = function(){
    if(checkBox.checked){
        gsap.to('#secondAddressTable', {
            duration: 0.7,
            height: secondAddressHeight,
        });
        for(var index=0;index < form1.length;index++){
          if(form1[index].id!="id_innerNum1"){
            form1[index].setAttribute("required", "''");
          }
        }
    }else{
        gsap.to('#secondAddressTable', {
            duration: 0.7,
            height: 0,
        });
        for(var index=0;index < form1.length;index++){
            form1[index].removeAttribute("required");
        }
    }
}

$(document).on('submit','#payment-form',function(e){
  e.preventDefault();
  $.ajax({
      type:'POST',
      url:'/checkout/',
      data:
      {
          name:$("#id_name").val(),
          lastname:$("#id_lastname").val(),
          country:$("#id_country").val(),
          street:$("#id_street").val(),
          city:$("#id_city").val(),
          region:$("#id_region").val(),
          postalCode:$("#id_postalCode").val(),
          email:$("#id_email").val(),
          phone:$("#id_phone").val(),
          name1:$("#id_name1").val(),
          lastname1:$("#id_lastname1").val(),
          country1:$("#id_country1").val(),
          street1:$("#id_street1").val(),
          city1:$("#id_city1").val(),
          region1:$("#id_region1").val(),
          postalCode1:$("#id_postalCode1").val(),
          email1:$("#id_email1").val(),
          phone1:$("#id_phone1").val(),
          csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
      },
      success:function(){
          
      }
  })
});

var stripe = Stripe('pk_test_tWdPJhSDh5uxSwQ17kCbsbML00aPZ3XI4g');
var elements = stripe.elements();

var elements = stripe.elements();
var style = {
  base: {
    color: "#2E5D4E",
    
  }
};

var card = elements.create("card", { style: style });
card.mount("#card-element");

card.on('change', function(event) {
    var displayError = document.getElementById('card-errors');
    if (event.error) {
      displayError.textContent = event.error.message;
    } else {
      displayError.textContent = '';
    }
  });


  var form = document.getElementById('payment-form');

form.addEventListener('submit', function(ev) {
  console.log("submitted");
  document.getElementById("fP").style.display="block";
  ev.preventDefault();
  // If the client secret was rendered server-side as a data-secret attribute
  // on the <form> element, you can retrieve it here by calling `form.dataset.secret`
  stripe.confirmCardPayment(cs, {
    payment_method: {
      card: card,
      billing_details: {
        name: document.getElementById("id_name").value + "" + document.getElementById("id_lastname").value,
      }
    }
  }).then(function(result) {
    if (result.error) {
      // Show error to your customer (e.g., insufficient funds)
      alert("Ups! " + result.error.message);
      document.getElementById("fP").style.display="none";
    } else {
      // The payment has been processed!
      if (result.paymentIntent.status === 'succeeded') {
        cart = {};
        localStorage.removeItem("cart");
        localStorage.removeItem("totalInCart");
        localStorage.removeItem("totalPrice");
        UpdateMini();
        window.location= "/succeed/";
        // Show a success message to your customer
        // There's a risk of the customer closing the window before callback
        // execution. Set up a webhook or plugin to listen for the
        // payment_intent.succeeded event that handles any business critical
        // post-payment actions.
      }
    }
  });
});
