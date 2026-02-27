def get_bag_quantity(request, product_slug):
    """
    Returns the total quantity of the products in the users bag
    Counts both products and pick and mix items in the session
    """
    total = 0

    bag = request.session.get('bag', {})
    if product_slug in bag and isinstance(bag[product_slug], int):
        total += bag[product_slug]

    pick_and_mix = request.session.get('pick_and_mix', {})
    pnm_items = pick_and_mix.get('items', {})

    if product_slug in pnm_items:
        total += pnm_items[product_slug].get('quantity', 0)

    return total
