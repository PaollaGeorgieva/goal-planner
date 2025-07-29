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
        queryset=Category.objects.all(),
        write_only=True,
        source='category'
    )

    class Meta:
        fields = [
            'id', 'title', 'description', 'start_date',
            'is_completed', 'category', 'category_id', 'goal_type'
        ]


class TargetGoalSerializer(BaseGoalSerializer):
    progress = serializers.SerializerMethodField()

    class Meta(BaseGoalSerializer.Meta):
        model = TargetGoal
        fields = BaseGoalSerializer.Meta.fields + [
            'end_date', 'completed_at', 'progress'
        ]
        read_only_fields = ['completed_at', 'progress']

    def get_progress(self, obj):
        return obj.progress_percent()


class HabitGoalSerializer(BaseGoalSerializer):
    progress = serializers.SerializerMethodField()

    class Meta(BaseGoalSerializer.Meta):
        model = HabitGoal
        fields = BaseGoalSerializer.Meta.fields + [
            'target_per_period', 'period_unit', 'completed_at', 'progress'
        ]
        read_only_fields = ['completed_at', 'progress']

    def get_progress(self, obj):
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