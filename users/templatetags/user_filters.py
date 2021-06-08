from django import template
register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={"class": css})


@register.filter
def recipe_ending(number, args):
    args = [arg.strip() for arg in args.split(',')]
    last_digit = int(number) % 10
    if last_digit == 1:
        return f'{number} {args[0]}'
    elif 1 < last_digit < 5:
        return f'{number} {args[1]}'
    elif last_digit > 4 or last_digit == 0:
        return f'{number} {args[2]}'


@register.filter
def is_basket(recipe_id, user):
    return user.basket.filter(id=recipe_id).exists()


@register.filter
def is_favorite(recipe_id, user):
    return user.favorites.filter(id=recipe_id).exists()


@register.filter
def is_following(author_id, user):
    return user.follow.filter(id=author_id).exists()


@register.filter
def is_tags(request, tag_id):
    new_request = request.GET.copy()
    tags = new_request.getlist('tag')
    if tag_id in tags:
        tags.remove(tag_id)
    else:
        tags.append(tag_id)

    new_request.setlist('tag', tags)
    return new_request.urlencode()


@register.simple_tag
def set_tags(request, tags, value):
    """Устанавливает get параметры в зависимости
    от выбранных тегов"""
    pass
    # request_object = request.GET.copy()
    # if request.GET.get(value):
    #     request_object.pop(value)
    # elif value in tags:
    #     for tag in tags:
    #         if tag != value:
    #             request_object[tag] = "tag"
    # else:
    #     request_object[value] = "tag"
    #
    # return request_object.urlencode()
