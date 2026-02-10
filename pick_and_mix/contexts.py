from pick_and_mix.models import PickAndMixBag


def pick_and_mix_content(request):
    current_pick_and_mix = request.session.get('pick_and_mix', {})
    pick_and_mix_bag = None
    total_weight = 0
    max_weight = 0
    bag_slug = None

    if request.resolver_match:
        bag_slug = request.resolver_match.kwargs.get('slug')

    # if current_pick_and_mix and bag_slug:
    #     if current_pick_and_mix.get('bag_slug')!= bag_slug:
    #         del request.session['pick_and_mix']
    #         current_pick_and_mix = None

    if current_pick_and_mix:
        pick_and_mix_bag = current_pick_and_mix
        total_weight = current_pick_and_mix.get('total_weight', 0)

        bag_id = current_pick_and_mix.get('bag_id')
        if bag_id:
            try:
                bag_obj = PickAndMixBag.objects.get(id=bag_id)
                max_weight = bag_obj.max_weight_in_grams
            except PickAndMixBag.DoesNotExist:
                max_weight = current_pick_and_mix.get('max_weight', 500)
    elif bag_slug:
        try:
            bag_obj = PickAndMixBag.objects.get(slug=bag_slug)
            max_weight = bag_obj.max_weight_in_grams
        except PickAndMixBag.DoesNotExist:
            max_weight = 0

    remaining_weight = max_weight - total_weight

    print('total weight', total_weight)
    print('max weight', max_weight)
    print('remaining weight', remaining_weight)

    return {
        'total_weight': total_weight,
        'max_weight': max_weight,
        'remaining_weight': remaining_weight,
        'pick_and_mix': pick_and_mix_bag,
    }
