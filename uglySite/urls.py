
from . import views
from django.urls import path



urlpatterns = [
    path('', views.landing, name="landing"),
    path('category/<str:categoryName>/', views.category, name="category"),
    path('product<int:identifier>/', views.product, name="product"),
    path('search/<str:text>/', views.search, name="search"),
    path('checkout/', views.checkout, name="checkout"),
    path('webhooks/stripe/', views.stripe_webhook, name='stripe-webhook'),
    path('succeed/', views.succeed, name="succeed"),
    path('error/', views.error, name="error"),
    path('loading/', views.loading, name="loading"),
    path('policy/', views.policy, name="policy"),
    path('extended-policy/', views.extendedPolicy, name="extendedPolicy"),
    path('shipping/', views.shipping, name="shipping"),
    path('hechopor/', views.madeby, name="madeby"),
    path('loadCustom/<str:ID>/', views.loadCustom, name="loadCustom"),
    #path('madeby/', vies.madeBy, name="madeBy")
]
