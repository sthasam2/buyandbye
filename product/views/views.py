from django.shortcuts import get_object_or_404, render

def home(request):
    return render(request, 'product/home.html')

def aboutus(request):
    """ About page """
    return render(request, 'product/about.html', {'title': 'About'})


def privacy_policy(request):
    """ PRIVACY POLICY page """
    return render(request, 'product/privacypolicy.html', {'title': 'Privacy Policy'})


def terms_and_conditions(request):
    """ TERMS AND CONDITION page """
    return render(request, 'product/terms_conditions.html', {'title': 'Terms and Conditions'})

