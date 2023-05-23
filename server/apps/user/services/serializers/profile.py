from server.apps.user.models import Profile


def update_profile_user(
    validated_data: dict,  # type: ignore
    instance: Profile,
) -> None:
    """Обновляем информацию о пользователе и его профиле."""
    first_name = validated_data.pop('first_name', '')
    last_name = validated_data.pop('last_name', '')
    update_fields = []
    Profile.objects.filter(pk=instance.pk).update(**validated_data)
    if first_name:
        instance.user.first_name = first_name
        update_fields.append('first_name')
    if last_name:
        instance.user.last_name = last_name
        update_fields.append('last_name')

    instance.user.save(update_fields=update_fields)
