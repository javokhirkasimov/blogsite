from .models import Category, Comment, Blog

def subject_renderer(request):
    data = {
        'all_categories': Category.objects.all()
    }
    return data

