from rest_framework.serializers import ValidationError


class YoutubeUrlValidator:
    """Валидатор для проверки, что ссылка указывает только на ресурсы YouTube."""

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        url = dict(value).get(self.field)
        if url:
            # Проверяем наличие 'youtube.com' или 'youtu.be' в ссылке
            if 'youtube.com' not in url:
                raise ValidationError({self.field: 'Разрешены только ссылки на youtube.com'})
