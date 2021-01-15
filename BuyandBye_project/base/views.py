from django.shortcuts import get_object_or_404, render

def home(request):
    return render(request, 'home.html')

def aboutus(request):
    """ About page """
    return render(request, 'about.html', {'title': 'About'})


def privacy_policy(request):
    """ PRIVACY POLICY page """
    return render(request, 'privacypolicy.html', {'title': 'Privacy Policy'})


def terms_and_conditions(request):
    """ TERMS AND CONDITION page """
    return render(request, 'terms_conditions.html', {'title': 'Terms and Conditions'})

