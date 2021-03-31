from .models import ActivityLog, Brand, Yeast


def logged_and_superuser(u): return u.is_authenticated and u.is_superuser


def yeast_order_by(request, queryset):
    ordering = request.GET.get('?sort')
    print(type(ordering))
    if ordering:
        return queryset.order_by(ordering, 'name')
    else:
        return queryset.order_by('name')


def model_shares(model):
    yeast_qty = len(Yeast.objects.all())

    def extract(instance):
        return {
            'name': instance.name,
            'share': int(len(instance.yeast_set.all()) / yeast_qty * 100),
            'url': instance.get_absolute_url(),
        }
    return map(extract, model.objects.all())


def check_model_gender(model):
    verbose_name = model._meta.verbose_name.lower()
    if verbose_name == 'perfil fermentativo':
        return 'um ' + verbose_name
    else:
        return 'uma ' + verbose_name


def creation_log(model, obj, user):
    activity = f"{user.first_name} {user.last_name} criou {check_model_gender(model)}: {obj.name}"
    log = ActivityLog(
        activity=activity,
        user=user
    )
    log.save()


def deletion_log(model, obj, user):
    activity = f"{user.first_name} {user.last_name} deletou {check_model_gender(model)}: {obj.name}"
    log = ActivityLog(
        activity=activity,
        user=user
    )
    log.save()


def reinnoculation_log(obj, user):
    activity = f"{user.first_name} {user.last_name} repicou uma levedura: {obj.name}"
    log = ActivityLog(
        activity=activity,
        user=user
    )
    log.save()
