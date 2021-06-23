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
def tags_filter(tags_list, tag):
    # if tags_list:
    new_list = tags_list.copy()
    if tag in tags_list:
        new_list.remove(str(tag))
    else:
        new_list.append(str(tag))
    return new_list
    # return tags_list

