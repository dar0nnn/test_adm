from .serializers import CategorySerializer
from .models import Category
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from pprint import pprint
import json

class CatView(APIView):
    """
    для GET запроса всех категорий и POST создания категорий
    """

    def get(self, request):
        """
        Получение всех категорий
        """
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        def create_childs(array_of_childs: list, parent: Category) -> Response:
            """
            Функция создает всех потомков рекурсивным методом. Немного костыльно, но ничего лучше не придумал.
            Чем то похоже на Flask.
            ::return Response status 201
            """
            for child in array_of_childs:
                inner_parent = Category.objects.create(name=child['name'], parent=parent)
                if 'children' in child:
                    create_childs(child['children'], inner_parent)
                else:
                    continue
            return Response(status=status.HTTP_201_CREATED)
     
        if not "name" in request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # создание родителя всех категорий
        parent = Category.objects.create(name=request.data['name'])
        if 'children' in request.data:      # создание потомков рекурсией
            create_childs(request.data['children'], parent)
        return Response(status=status.HTTP_201_CREATED)


class CatDetailView(APIView):
    """
    Для GET запроса по ключу и DELETE запроса по ключу
    """

    def get(self, request, pk):

        def get_parents(category: Category, listOfParents=[]) -> list:
            """
            Ищет родителей для определенной категории.
            Опять же ничего лучше не придумал
            ::return list: список родителей категории
            """
            cat = get_object_or_404(Category, pk=category.id)
            listOfParents.append(
                {'id': cat.id, 'name': cat.name})
            if cat.parent:
                get_parents(cat.parent)
            return listOfParents
        
        def get_siblings(category: Category, sibling_list = []) -> list:
            """
            Ищет соседей заданой категории
            ::return list: список соседей
            """
            siblings = Category.objects.filter(parent=category.parent)
            for sibling in siblings:
                if sibling.name == category.name:
                    continue
                sibling_list.append({'id':sibling.id, 'name': sibling.name})
            return sibling_list

        category = get_object_or_404(Category, pk=pk)
        # проверка на родителя и подготовка словарей с данными
        data = {"id": category.id, 'name': category.name,
                "children": [], 'parents': [], 'siblings':[]}
        if category.parent:
            parentList = get_parents(category.parent)
            data['parents'] = parentList
            data['siblings'] = get_siblings(category)
        for c in category.get_descendants(include_self=False):
            child = get_object_or_404(Category, pk=c.id)
            if child.parent.id != data['id']: # поиск ближайших потомков
                break                         # чтобы не было всех потомков по цепочке
            data['children'].append({'id': child.id, 'name': child.name})
        return Response(data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        cat = get_object_or_404(Category, pk=pk)
        cat.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
