if x:
    pprin(salom)
elif x[char_val].lower() in chars_list:
    atr_old_ids = Characteristics.objects.filter(name=x[char_val].lower())
    atr_old_list = []
    for atr in atr_old_ids:
        atr_old_list.append(atr.attribute_id)
        if int(attr_id[f'{sub_name}']) not in atr_old_list:
            # print('yes')
            # print(f"new={attr_id[f'{sub_name}']}")
            # print(atr_old_list)
            slug = self.get_slugify(f'{x[char_val].lower()}')
            p = Characteristics(
                slug=slug,
                name=x[char_val].lower(),
                created_at='2021-05-29 00:55:49',
                updated_at='2021-05-20 21:05:09',
                deleted_at=None,
            ).save()
            char_id = Characteristics.objects.filter(name=x[char_val].lower())[:1].get().id
            self.char_translation(char_id, name=x[char_val].lower())