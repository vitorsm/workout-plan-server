

def merge_lists(persisted_items: list, new_items: list):
    if not new_items:
        __remove_all_list_items(persisted_items)
        return

    # adding or merging items
    for new_item in new_items:
        persisted_item = __find_item_in_list(persisted_items, new_item)
        if persisted_item:
            persisted_item.merge_model(new_item)
        else:
            persisted_items.append(new_item)

    # removing items
    for persisted_item in persisted_items:
        new_item = __find_item_in_list(new_items, persisted_item)
        if not new_item:
            persisted_items.remove(persisted_item)


def __find_item_in_list(items: list, item_to_find):
    return next((item for item in items if item == item_to_find), None)


def __remove_all_list_items(items: list):
    count = len(items)
    for index in range(count):
        items.remove(0)
