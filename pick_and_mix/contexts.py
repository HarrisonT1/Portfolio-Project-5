def pick_and_mix_content(request):
    pick_and_mix = request.session.get('pick_and_mix', {})

    if not pick_and_mix:
        return {
            'pick_and_mix': None,
            'remaining_weight': None,
        }

    total = pick_and_mix.get('total_weight', 0)
    max_weight = pick_and_mix.get('max_weight', 0)

    return {
        'remaining_weight': max_weight - total,
        'pick_and_mix': pick_and_mix
    }
