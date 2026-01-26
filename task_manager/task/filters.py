import django_filters
from django.contrib.auth import get_user_model
from .models import Task, Status, Label

User = get_user_model()

class TaskFilter(django_filters.FilterSet): 
    # Фильтр по статусу (выпадающий список статусов)
    status = django_filters.ModelChoiceFilter(
        queryset=Status.objects.all(), label='Статус'
        )
    
    # Фильтр по исполнителю (выпадающий список пользователей)
    executor = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(), label='Исполнитель'
        )
    
    # Фильтр по метке (выпадающий список меток)
    label = django_filters.ModelChoiceFilter(
        queryset=Label.objects.all(), label='Метка'
        )
    
    # Дополнительный чекбокс/фильтр для "Только мои задачи"
    # Этот фильтр нужно обрабатывать немного иначе в представлении, 
    # но можно добавить базовую логику через custom filter:

    class Meta:
        model = Task
        # Явно указываем поля, которые будем фильтровать
        fields = ['status', 'executor', 'label'] 
