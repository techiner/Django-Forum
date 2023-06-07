from django.db.models import Count, OuterRef, Subquery
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

from forum.models import Forum, Message

# @login_required
def homePageView(request):
    
    last_msg_subquery = Message.objects.filter(topic__forum__id=OuterRef('pk')).order_by('-creation_date')[:1]
    queryset = Forum.objects \
        .annotate(topic_cnt=Count('topic')) \
        .annotate(msg_cnt=Count('topic__message')) \
        .annotate(last_msg_date=Subquery(last_msg_subquery.values('creation_date'))) \
        .annotate(last_msg_topic=Subquery(last_msg_subquery.values('topic__title'))) \
        .annotate(last_msg_user=Subquery(last_msg_subquery.values('author__username')))

    return render(request, 'forum/forums.html', {"forums": queryset})


# Create your views here.
