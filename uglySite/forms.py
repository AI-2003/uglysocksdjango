from django import forms
from .models import Review, Order

class SearchForm(forms.Form):
    text = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Buscar'}))

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['reviewer', 'email', 'review']

class CheckoutForm(forms.Form):
    name = forms.CharField(label='Nombre(s)', max_length=100)
    lastname = forms.CharField(label='Apellidos', max_length=100)
    country = forms.CharField(label='País', max_length=150)
    city = forms.CharField(label='Ciudad', max_length=150)
    region = forms.CharField(label='Región/Provincia', max_length=150)
    street = forms.CharField(label='Calle y número (ext)', max_length=150)
    innerNum = forms.IntegerField(label='Número interior', required=False)
    postalCode = forms.IntegerField(label='Código Postal')
    email = forms.EmailField(label='Correo electrónico', max_length=254)
    phone = forms.CharField(label='Teléfono', max_length=150)


class CheckoutForm1(forms.Form):
    name1 = forms.CharField(label='Nombre(s)', max_length=100)
    lastname1 = forms.CharField(label='Apellidos', max_length=100)
    country1 = forms.CharField(label='País', max_length=150)
    city1 = forms.CharField(label='Ciudad', max_length=150)
    region1 = forms.CharField(label='Región/Provincia', max_length=150)
    street1 = forms.CharField(label='Calle y número (ext)', max_length=150)
    innerNum1 = forms.IntegerField(label='Número interior', required=False)
    postalCode1 = forms.IntegerField(label='Código Postal')
    email1 = forms.EmailField(label='Correo electrónico', max_length=254)
    phone1 = forms.CharField(label='Teléfono', max_length=150)

    def __init__(self, *args, **kwargs):
        super(CheckoutForm1, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form1'

class CartForm(forms.Form):
    addToCart = forms.IntegerField(label='', required=True, widget=forms.NumberInput(attrs={'id':'cartQuantity','value': '1'}))

class CustomImagesForm(forms.Form):
    front = forms.ImageField(label="Frente", required=False, widget=forms.ClearableFileInput(attrs={'onchange': 'loadFront(event)', }))
    back = forms.ImageField(label="Atrás", required=False, widget=forms.ClearableFileInput(attrs={'onchange': 'loadBack(event)', }))

    

class CustomImagesURLForm(forms.Form):
    fronturl = forms.CharField(required=False)
    backurl = forms.CharField(required=False)
    uuid = forms.UUIDField(required=False)