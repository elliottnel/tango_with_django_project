from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from rango.models import Category ,Page
from rango.forms import CategoryForm
from django.shortcuts import render, redirect
from rango.forms import PageForm
from django.urls import reverse


def show_category(request, category_name_slug):

    context_dict = {}
    try:

        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)
# Adds our results list to the template context under name pages.
        context_dict['pages'] = pages

        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None
    return render(request, 'rango/category.html', context=context_dict)

def index(request):

    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage matches to {{ boldmessage }} in the template!
    most_viewed_pages = Page.objects.order_by('-views')[:5]


    category_list = Category.objects.order_by('-likes')[:5]

    context_dict = {}
    context_dict = {'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!'}
    context_dict['categories'] = category_list
    context_dict['pages'] = most_viewed_pages

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render(request, 'rango/index.html', context=context_dict)



def about(request):
    context_dict = {'boldmessage' : 'Elliott'}
    return render(request, 'rango/about.html', context=context_dict)

def add_category(request):
    form = CategoryForm()

    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)

            # Now that the category is saved, redirect the user.
            return redirect('/rango/')
        else:
            # The supplied form contained errors.
            # Just print them to the terminal.
            print(form.errors)

    # Will handle the bad form, new form, or no form supplied cases.
    # Render the form with error messages (if any).
    return render(request, 'rango/add_category.html', {'form': form})

def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    # You cannot add a page to a Category that does not exist...
    if category is None:
        return redirect('/rango/')

    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            page = form.save(commit=False)
            page.category = category
            page.views = 0
            page.save()

            return redirect(
                reverse(
                    'rango:show_category',
                    kwargs={'category_name_slug': category_name_slug}
                )
            )
        else:
            print(form.errors)

    context_dict = {
        'form': form,
        'category': category
    }

    return render(request, 'rango/add_page.html', context=context_dict)