# it's good just because it's exactly the same data but surely there is space for improvements
def populate_form_with_object_data(form, obj):
    form.name.data = obj.name
    form.city.data = obj.city
    form.state.data = obj.state
    form.phone.data = obj.phone
    form.genres.data = [str(i.id) for i in obj.genres_relation]
    form.website.data = obj.website
    form.facebook_link.data = obj.facebook_link
    form.image_link.data = obj.image_link
    form.seeking_description.data = obj.seeking_description
    # ignore address as it's the only value that's different between Venue, and Artist
    try:
        form.address.data = obj.address
    except AttributeError:
        pass


def populate_object_with_form_data(obj, form, genres_ids):
    def value_or_none(v):
        return v if len(v) else None

    obj.name = form.name.data
    obj.city = form.city.data
    obj.state = form.state.data
    obj.phone = value_or_none(form.phone.data)
    obj.image_link = form.image_link.data
    obj.facebook_link = value_or_none(form.facebook_link.data)
    obj.website = value_or_none(form.website.data)
    obj.seeking_description = value_or_none(form.seeking_description.data)
    obj.genres_relation = genres_ids
    # ignore address as it's the only value that's different between Venue, and Artist
    try:
        obj.address = form.address.data
    except AttributeError:
        pass
