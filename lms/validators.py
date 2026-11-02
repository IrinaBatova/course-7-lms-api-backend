from rest_framework.exceptions import ValidationError

def validate_youtube_link(value):
    """
    Проверяет, что если в поле передана ссылка, то она ведет строго на youtube.com
    """
    if value:
        # Переводим в нижний регистр
        link = str(value).lower()

        # Если в ссылке нет упоминания youtube.com
        if 'youtube.com' not in link and 'youtu.be' not in link:
            raise ValidationError('Разрешены ссылки только на видеохостинг youtube.com!')