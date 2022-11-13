from django.shortcuts import render, get_object_or_404
from django.db.models import Q
# Create your views here.
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Schemes,Tags, Category
from django.urls import reverse_lazy
from django.forms.widgets import SelectDateWidget
# from taggit.models import Tags,Category,SubCategory

def home(request):
    # context = {
    #     'posts': Schemes.objects.all()
    # }
    return render(request, 'schemes/home.html')

class SchemeListView(ListView):
    model = Schemes
    template_name = 'schemes/schemes_list.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'schemes'
    ordering = ['uploadDate']
    paginate_by = 8
    queryset = model.objects.all()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # # context['tasks'] = context['tasks'].filter(user=self.request.user)
        # context['count'] = context['tasks'].filter(complete=False).count()

        search_input = self.request.GET.get('search-area') or ''
        # if search_input:
        #     context['schemes'] = Schemes.objects.filter(details__icontains=search_input)
        # paginate_by = 8
        context['title'] = 'Search Schemes'
        context['search_input']= search_input
        print('Checking',search_input,context)
        return context
    def get_queryset(self):
        # user = get_object_or_404(User, username=self.kwargs.get('username'))
        search_input = self.request.GET.get('search-area') or ''
        return Schemes.objects.filter(details__icontains=search_input).order_by('-uploadDate')

    

class SchemeDetailView(DetailView):
    model = Schemes
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context,'Hello')
        # context["title"] = context['schemes'].objects
        fields = ['title','name','brief','eligibility','references','slug','tags','details','category','subcategory','openDate','closeDate']
        context['fields']=fields
        return context

class SchemeAdd(CreateView):
    model = Schemes
    fields = ['title','name','brief','eligibility','references','slug','tags','details','category','subcategory','openDate','closeDate']
    # success_url = reverse_lazy('tasks')
    success_url = reverse_lazy('schemes')
    def get_form(self,form_class=None):
        form = super(SchemeAdd,self).get_form(form_class)
        form.fields['openDate'].widget = SelectDateWidget()
        form.fields['closeDate'].widget = SelectDateWidget()
        return form
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(SchemeAdd,self).form_valid(form)

# class CategoryListView(ListView,slug):
#     tag = get_object_or_404(Tags,slug=slug)
def tagged(request, slug):
    tag = get_object_or_404(Category, slug=slug)
    # Filter posts by tag name  
    posts = Schemes.objects.filter(category=tag)
    context = {
        'tag':tag,
        'schemes':posts,
    }
    return render(request, 'schemes/schemes_list.html', context)
