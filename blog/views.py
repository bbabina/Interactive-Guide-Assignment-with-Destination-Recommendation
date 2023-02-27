from calendar import c
from inspect import BlockFinder
from django.shortcuts import redirect, render

from destination.models import Places
from .models import Blog, Blogimages
from django.views import generic
from .forms import createblogpostform
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required 

# Create your views here.
@method_decorator(login_required, name='dispatch')
class bloglistview(generic.ListView):
    model= Blog
    template_name= 'blog/blog_list.html'
    
    
class blogdetailview(generic.DetailView):
    model= Blog
    template_name= 'blog/blogpost_view.html'
    def get_context_data(self, *args, **kwargs):
        context = super(blogdetailview, self).get_context_data(*args, **kwargs)
        user=self.request.user
        context['images'] = Blogimages.objects.all()
       

        return context
       

@login_required
def add_blogview(request,p_id):
    if request.method=='POST':
        form=createblogpostform(request.POST or None,request.FILES or None)
        images=request.FILES.getlist('images')
        description = request.POST.get('post')
        if form.is_valid():
            data=Blog()
            data.related_place_id=p_id
            data.title=form.cleaned_data['title']
            data.description=description
            data.author=request.user
            data.thumbnail=form.cleaned_data['thumbnail']
            data.save()
            if(len(images)==0):
                Blogimages.objects.create(bg_id=data.id,image=data.thumbnail)
            else:
                for f in images:
                    Blogimages.objects.create(bg_id=data.id,image=f)
               
            
            return redirect('placeview' , p_id)   
            
    else:
        form=createblogpostform()
        
    return render(request,'blog/postblog.html',{'form':form , 'place': Places.objects.get(id=p_id)})          

     

