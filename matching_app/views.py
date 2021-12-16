from django.db.models import Count
from rest_framework.response import Response
from . import models
from rest_framework import viewsets
from rest_framework.decorators import action
from . import serializers
from django.views import generic
from accounts.models import CustomUser
from accounts.views import IsAdminOrIsSelf
import os

# Create your views here.
class TopPageView(generic.TemplateView):
    template_name = "matching_app/index.html"
    

#たける
def get_ranking():
    games = {}
    for obj in models.Talkroom.objects.annotate(Count('guest_user')):
        if  obj.game not in games.keys():
            games[obj.game] = obj.guest_user__count + 1
        else:
            games[obj.game] = games[obj.game]+obj.guest_user__count + 1
    sorted_games = sorted(games.items(), key=lambda x:x[1],reverse=True)
    return [x[0] for x in sorted_games] + [y for y in models.Game.objects.all()[:10-len(sorted_games)]]


class GameViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.GameItemSerializer
    def get_queryset(self):
        queryset = models.Game.objects.all()[:10]
        return queryset
    
    def talk_ratio(self,pk):
        talkroom_people = models.Talkroom.objects.filter(game=pk).aggregate(Count('guest_user'))
        all_talkroom = models.Talkroom.objects.filter(game=pk).count()
        ratio_data = {
            "guest":talkroom_people["guest_user__count"],
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
        serializer = serializers.GameItemSerializer(queryset)
        response_data= serializer.data
        response_data.update(self.talk_ratio(pk))
        return Response(response_data)


#たける
class TalkViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TalkItemSerializer
    def get_queryset(self):
        user = self.request.user
        try:
            talkroom = models.Talkroom.objects.get(host_user = user.pk)
        except models.Talkroom.DoesNotExist:
            talkroom = models.Talkroom.objects.get(guest_user__pk = user.pk)
        queryset = models.Talk.objects.filter(talkroom = talkroom)
        return queryset

    def list(self, request):
        user = request.user
        try:
            talkroom = models.Talkroom.objects.get(host_user = user.pk)
        except models.Talkroom.DoesNotExist:
            talkroom = models.Talkroom.objects.get(guest_user__pk = user.pk)
        queryset = models.Talk.objects.filter(talkroom = talkroom)
        serializer = serializers.TalkItemSerializer(queryset,many=True)
        for x in serializer.data:
            user = CustomUser.objects.get(pk=x["user"])
            x.update({"user":{
                "user_id":user.pk,
                "user_name":user.username,
                "user_image":str(user.image)
            }})
        return Response(serializer.data)
    
    def create(self, request):
        user = request.user
        try:
            talkroom = models.Talkroom.objects.get(host_user = user.pk)
        except models.Talkroom.DoesNotExist:
            talkroom = models.Talkroom.objects.get(guest_user__pk = user.pk)
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
        response_data = serializer.data
        users_info = []
        for x in response_data["guest_user"]:
            user = CustomUser.objects.get(pk=x)
            users_info.append({
                "user_id":x,
                "user_name":user.username,
                "user_image":str(user.image),
                "user_introduction":user.introduction
            })
        response_data["guest_user"] = users_info
        host_user = queryset.host_user
        response_data["host_user"] = {
            "user_id":host_user.pk,
            "user_name":host_user.username,
            "user_image":str(host_user.image),
            "user_introduction":host_user.introduction
        }
        return Response(response_data)

    def create(self,request):
        serializer = serializers.TalkroomItemSerializer(data=request.data,context={'userID':request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

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
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdminOrIsSelf])
    def join_talkroom(self, request, pk=None):
        talkroom = models.Talkroom.objects.get(pk=pk)
        talkroom.guest_user.add(request.user)
        users_num = talkroom.guest_user.all().count()
        if users_num >= talkroom.recruit_num:
            talkroom.under_recruitment = False
        talkroom.save()
        serializer = serializers.TalkroomItemSerializer(talkroom)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdminOrIsSelf])
    def exit_talkroom(self, request, pk=None):
        talkroom = models.Talkroom.objects.get(pk=pk)
        if request.user == talkroom.host_user or talkroom.guest_user.all().count() < 1:
            talks = models.Talk.objects.filter(talkroom = talkroom)
            for talk in talks:
                if talk.talkfile is not None:
                    os.remove(talk.talkfile.path)
            talkroom.delete()
            return Response({"detail":"deleted"})
        talkroom.guest_user.remove(request.user)
        talkroom.save()
        serializer = serializers.TalkroomItemSerializer(talkroom)
        return Response(serializer.data)


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

