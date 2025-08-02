from django.db.models import Q
from rest_framework import serializers

from goals.models import Category, TargetGoal, HabitGoal, HabitCheck
from notes.models import Note
from steps.models import Step


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'is_system']


class BaseGoalSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.none(),
        write_only=True,
        source='category',
        allow_null=True,
        required=False,
        default=None,
    )

    new_category = serializers.CharField(
        write_only=True,
        required=False,
        allow_blank=True,
        max_length=100
    )

    class Meta:
        model = None
        fields = [
            'id', 'title', 'description', 'start_date', 'category', 'category_id', 'new_category',
        ]
        read_only_fields = ['id', 'is_completed', 'category']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.context['request'].user
        allowed_categories = Category.objects.filter(
            Q(is_system=True) | Q(created_by=user)
        )
        self.fields['category_id'].queryset = allowed_categories

    def validate(self, data):
        selected_category = data.get('category')
        new_name = data.get('new_category', '').strip()

        if new_name:
            if Category.objects.filter(name__iexact=new_name, is_system=True).exists():
                raise serializers.ValidationError({'new_category': 'This system category already exists.'})
            if Category.objects.filter(name__iexact=new_name, created_by=self.context['request'].user).exists():
                raise serializers.ValidationError({'new_category': 'You already created a category with this name.'})

        if bool(selected_category) == bool(new_name):
            error = {'category_id': 'Provide exactly one of category_id or new_category.'}
            raise serializers.ValidationError(error)

        return data

    @staticmethod

    def create_category(name, user):
        return Category.objects.create(name=name, created_by=user, is_system=False)

    def create(self, validated_data):
        new_name = validated_data.pop('new_category', '').strip()
        if new_name:
            validated_data['category'] = self.create_category(new_name, self.context['request'].user)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        new_name = validated_data.pop('new_category', '').strip()
        if new_name:
            validated_data['category'] = self.create_category(new_name, self.context['request'].user)
        return super().update(instance, validated_data)


class TargetGoalSerializer(BaseGoalSerializer):
    progress = serializers.SerializerMethodField()


    class Meta(BaseGoalSerializer.Meta):
        model = TargetGoal
        fields = BaseGoalSerializer.Meta.fields + ['end_date', 'completed_at', 'progress']
        read_only_fields = BaseGoalSerializer.Meta.read_only_fields + ['completed_at', 'progress', 'goal_type']

    def create(self, validated_data):

        validated_data['goal_type'] = TargetGoal.TYPE_CHOICES[0][0]
        return super().create(validated_data)

    @staticmethod
    def get_progress(obj):
        return obj.progress_percent()



class HabitGoalSerializer(BaseGoalSerializer):
    progress = serializers.SerializerMethodField()

    class Meta(BaseGoalSerializer.Meta):
        model = HabitGoal
        fields = BaseGoalSerializer.Meta.fields + ['target_per_period', 'period_unit', 'completed_at', 'progress']
        read_only_fields = BaseGoalSerializer.Meta.read_only_fields + ['completed_at', 'progress', 'goal_type']

    def create(self, validated_data):
        validated_data['goal_type'] = HabitGoal.TYPE_CHOICES[1][0]
        return super().create(validated_data)

    @staticmethod
    def get_progress(obj):
        return obj.progress_percent()



class StepSerializer(serializers.ModelSerializer):
    class Meta:
        model = Step
        fields = ['id', 'title', 'completed', 'completed_at']
        read_only_fields = ['completed_at']


class HabitCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = HabitCheck
        fields = ['id', 'date']


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['id', 'title', 'content', 'image', 'created_at']
        read_only_fields = ['created_at']