def save_get(self, records, model, scenario):
    save_all(records, model)
    return get_all(model, scenario)


def save_all(records, model):
    for record in records:
        record.full_clean()  # call full clean on each record
    model.objects.bulk_create(records)  # save to the database


def get_all(model, scenario):
    """
    :param model: a database model with fields scenario and name which are unique together
    :return: a dictionary of the fields of the given model corresponding to the current simulation,
     with their name fields as key.
    """
    records = model.objects.filter(scenario=scenario)
    return {record.name: record for record in records}