from api_service.models import Organisation, Owner, Phone


def end_dot(text: str) -> str:
    return text.strip(". \n\t") + "."


def comma_space(text: str) -> str:
    return ", ".join(map(lambda word: word.strip(), text.split(",")))


def create_records(item):
    organisation, _ = Organisation.objects.get_or_create(
        title=item["title"],
        object_type=item["object_type"],
        address=item["address"],
        latitude=item["latitude"],
        longitude=item["longitude"],
        description=item["description"],
    )
    Owner.objects.get_or_create(
        owner=item["owner"],
        organisation=organisation,
    )
    Phone.objects.get_or_create(
        phone=item["phone"],
        organisation=organisation,
    )
