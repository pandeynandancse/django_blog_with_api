try:
    from urllib import quote_plus #python 2
except:
    pass

try:
    from urllib.parse import quote_plus #python 3
except: 
    pass

from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .forms import PostForm
from .models import Post

def post_create(request):
	if not request.user.is_staff or not request.user.is_superuser:  #it automatically assumes the admin as  logged in user by default 
		raise Http404
		

	#checks if user is logged in 
	# if request.user.is_authenticated():
	# 	raise Http404
		



	#request.POST or None ==>> post_form.html is rendered  only by clicking some button that means via post request ==>> ' None ' is used because if we don't use it then first time also when form is rendered it says 'field
    #is required' but we want to render it only after in-valid argument so used it.
	form = PostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.user = request.user
		instance.save()
		# message success
		messages.success(request, "Successfully Created")
		return HttpResponseRedirect(instance.get_absolute_url())
	context = {
		"form": form,
	}
	return render(request, "post_form.html", context)

'''
Created for Django Code Review
'''

from django.views.generic import DetailView

class PostDetailView(DetailView):
	template_name = 'post_detail.html' 
	
	def get_object(self, *args, **kwargs):
		slug = self.kwargs.get("slug")
		instance = get_object_or_404(Post, slug=slug)
		if instance.publish > timezone.now().date() or instance.draft:
			if not self.request.user.is_staff or not self.request.user.is_superuser:
				raise Http404
		return instance
	
	def get_context_data(self, *args, **kwargs):
		context = super(PostDetailView, self).get_context_data(*args, **kwargs)
		instance = context['object']
		context['share_string'] = quote_plus(instance.content)
		return context
	
# in posts/urls.py --> PostDetailView.as_view() instead of post_detail


def post_detail(request, slug=None):
	# instance = get_object_or_404(Post, id =3) #querying by id is not a good approach becoz id acan be missing for some posts if that post  has been deleted
	instance = get_object_or_404(Post, slug=slug)    #get_object_or_404 function 
	

	if instance.publish > timezone.now().date() or instance.draft:
		if not request.user.is_staff or not request.user.is_superuser:
			raise Http404
	share_string = quote_plus(instance.content)
	context = {
		"title": instance.title,
		"instance": instance,
		"share_string": share_string,
	}
	return render(request, "post_detail.html", context)

def post_list(request):
	today = timezone.now().date()
	queryset_list = Post.objects.active() #.order_by("-timestamp")
	if request.user.is_staff or request.user.is_superuser:
		queryset_list = Post.objects.all()
	
	query = request.GET.get("q")
	if query:
		# for searching posts ==>> Hints.txt topic 32  ==>via get request
		queryset_list = queryset_list.filter(
				Q(title__icontains=query)|
				Q(content__icontains=query)|
				Q(user__first_name__icontains=query) |
				Q(user__last_name__icontains=query)
				).distinct()
	paginator = Paginator(queryset_list, 8) # Show 25 contacts per page
	page_request_var = "page"
	page = request.GET.get(page_request_var)
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		queryset = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		queryset = paginator.page(paginator.num_pages)


	context = {
		"object_list": queryset, 
		"title": "List",
		"page_request_var": page_request_var,
		"today": today,
	}
	return render(request, "post_list.html", context)





def post_update(request, slug=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance = get_object_or_404(Post, slug=slug)
	form = PostForm(request.POST or None, request.FILES or None, instance=instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		messages.success(request, "<a href='#'>Item</a> Saved", extra_tags='html_safe')
		return HttpResponseRedirect(instance.get_absolute_url())  # redirects to post_details page becoz of get_absolute_url() with  messages as  argument  ==>> see post+details for more info.
	context = {
		"title": instance.title,
		"instance": instance,
		"form":form,
	}
	return render(request, "post_form.html", context)



def post_delete(request, slug=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance = get_object_or_404(Post, slug=slug)
	instance.delete()
	messages.success(request, "Successfully deleted")
	return redirect("posts:list")


def post_home(request):
	HttpResponse("<h1>dad</h1>")