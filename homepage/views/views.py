from django.shortcuts import get_object_or_404, render

def home(request):
    return render(request, 'homepage/home.html')

def aboutus(request):
    """ About page """
    return render(request, 'homepage/about.html', {'title': 'About'})


def privacy_policy(request):
    """ PRIVACY POLICY page """
    return render(request, 'homepage/privacypolicy.html', {'title': 'Privacy Policy'})


def terms_and_conditions(request):
    """ TERMS AND CONDITION page """
    return render(request, 'homepage/terms_conditions.html', {'title': 'Terms and Conditions'})

