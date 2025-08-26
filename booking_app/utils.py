from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def paginate_objects(request, queryset, items_per_page):
    paginator = Paginator(queryset, items_per_page)
    page = request.GET.get('page')

    try:
        objects_page = paginator.page(page)
    except PageNotAnInteger:
        objects_page = paginator.page(1)
    except EmptyPage:
        objects_page = paginator.page(paginator.num_pages)

    return objects_page, paginator
