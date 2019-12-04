from django.shortcuts import render

posts=[
    {
        'author' : 'Sambeg',
        'title': 'Blog Post',
        'content': '1st post content'
    },
    {
        'author': 'Sambeg',
        'title': 'Blog Post',
        'content': '2nd post content'
    }

]

def home(request):
    context={
        'displayContent':posts
    }
    return render(request, 'homepage/home.html', context)

def aboutus(request):
    return render(request, 'homepage/about.html', {'title': 'About'})
