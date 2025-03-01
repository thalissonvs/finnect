from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer as DjoserUserCreateSerializer

User = get_user_model()


class UserCreateSerializer(DjoserUserCreateSerializer):
    class Meta(DjoserUserCreateSerializer.Meta):
        model = User
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "id_number",
            "last_name",
            "security_question",
            "security_answer",
            "password",
        )
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user