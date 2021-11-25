from django.db.models import Count
from rest_framework.response import Response
from . import models
from rest_framework import viewsets
from . import serializers
from django.views import generic

# Create your views here.
class TopPageView(generic.TemplateView):
    template_name = "matching_app/index.html"
    

#たける
def get_ranking():
    games = {}
    for obj in models.Talkroom.objects.annotate(Count('users_ID')):
        if  obj.game not in games.keys():
            games[obj.game] = obj.users_ID__count
        else:
            games[obj.game] = games[obj.game]+obj.users_ID__count
    sorted_games = sorted(games.items(), key=lambda x:x[1],reverse=True)
    return [x[0] for x in sorted_games] + [y for y in models.Game.objects.all()[:10-len(sorted_games)]]


class GameViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.GameItemSerializer
    def get_queryset(self):
        queryset = models.Game.objects.all()[:10]
        return queryset
    
    def talk_ratio(self):
        talkroom_people = models.Talkroom.objects.all().aggregate(Count('users_ID'))
        all_talkroom = models.Talkroom.objects.count()
        ratio_data = {
            "all":talkroom_people,
            "host":all_talkroom,
        }
        return ratio_data
    
    def list(self, request):
        #ranking
        queryset = get_ranking()        
        keyword = self.request.query_params.get('search')
        if keyword is not None:
            name_qs = models.Game.objects.filter(game_name__icontains=keyword)
            detail_qs = models.Game.objects.filter(detail__icontains=keyword)
            genre_qs = models.Game.objects.filter(genre__genrename__icontains=keyword)
            tags_qs = models.Game.objects.filter(tags__tag_name__icontains=keyword)
            queryset = name_qs.union(detail_qs,genre_qs,tags_qs)
        serializer = serializers.GameItemSerializer(queryset,many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        queryset = models.Game.objects.get(pk=pk)
        ratio_data = self.talk_ratio()
        serializer = serializers.GameItemSerializer(queryset,context={"host_ratio":ratio_data["host"],"all_count":ratio_data["all"]})
        return Response(serializer.data)


#たける
class TalkViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TalkItemSerializer
    def get_queryset(self):
        user = self.request.user
        talkroom = models.Talkroom.objects.get(users_ID__pk = user.pk)
        queryset = models.Talk.objects.filter(talkroom = talkroom)
        return queryset
    
    def create(self, request):
        user = request.user
        talkroom = models.Talkroom.objects.get(users_ID__pk = user.pk)
        serializer = serializers.TalkItemSerializer(data=request.data,context={'userID':user,'talkroom':talkroom})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
        

#宋
class TalkroomViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TalkroomItemSerializer
    def get_queryset(self):
        inquiry = models.Inquiry.objects.filter(userID=self.request.user)
        return inquiry

    #ページネーション未実装
    def list(self, request):
        user = request.user
        gender = user.gender
        queryset = models.Talkroom.objects.filter(under_recruitment=True).exclude(recruit_gender="FE")
        if gender == "EX":
            queryset = models.Talkroom.objects.filter(under_recruitment=True,recruit_gender="AL")
        elif gender =="FE":
            queryset = models.Talkroom.objects.filter(under_recruitment=True).exclude(recruit_gender="MA")
        serializer = serializers.TalkroomItemSerializer(queryset,many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        queryset = models.Talkroom.objects.get(pk=pk)
        serializer = serializers.TalkroomItemSerializer(queryset)
        return Response(serializer.data)

    def create(self,request):
        serializer = serializers.TalkroomItemSerializer(data=request.data,context={'userID':request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=200)

    def partial_update(self, request, pk=None):
        talkroom = models.Talkroom.objects.get(pk=pk)
        serializer = serializers.TalkroomItemSerializer(talkroom,data=request.data,partial=True,context={'userID':request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def destroy(self, request, pk=None):
        queryset = models.Talkroom.objects.get(pk=pk)
        data = queryset.delete()
        return Response(data)


#宋
class InquiryViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.InquiryItemSerializer
    def get_queryset(self):
        inquiry = models.Inquiry.objects.filter(userID=self.request.user)
        return inquiry
    
    def create(self,request):
        serializer = serializers.InquiryItemSerializer(data=request.data, context={'userID':request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=200)

