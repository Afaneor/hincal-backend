from server.apps.hincal.models import Report


def add_offers_and_wishes_in_context(
    report: Report,
    data: dict,
) -> None:
    """Формирование предложений и мер поддержки."""
    report_context = report.context

    if report_context.get('context_for_file').get('offers_and_wishes'):
        return

    areas = ''
    supports = ''
    offers = ''
    for key_dict, value_dict in data.items():
        if key_dict == 'areas':
            for en_index, area in enumerate(value_dict[:1]):
                areas += (
                    f'Площадка № {en_index}:\n' +
                    f"Название: {area.get('title')}\n" +
                    f"Адрес: {area.get('address')}\n" +
                    f"Подробнее: {area.get('site')}\n"
                )

        if key_dict == 'supports':
            for en_index, support in enumerate(value_dict[0:1]):  # noqa: WPS440
                supports += (
                    f'Мера поддержки № {en_index}:\n' +
                    f"Название: {support.get('title')}\n" +
                    f"Описание: {support.get('text')}\n" +
                    f"Сумма субсидий: {support.get('amount')}\n" +
                    f"Подробнее: {support.get('site')}\n"
                )

        if key_dict == 'offers':
            for en_index, offer in enumerate(value_dict[:1]):  # noqa: WPS440
                offers += (
                    f'Партнерское предложение № {en_index}:\n' +
                    f"Название: {offer.get('title')}\n" +
                    f"Процентная ставка: {offer.get('interest_rate')}\n" +
                    f"Срок займа{offer.get('loan_term')}\n" +
                    f"amount{offer.get('amount')}\n" +
                    f"Подробнее: {offer.get('site')}\n"
                )

    report_context.get('context_for_file').update(
        {
            'offers_and_wishes': (
                'Площадки для создания промышленного предприятия:\n' +
                areas + '\n\n' +
                'Меры по поддержке промышленных предприятий:\n' +
                supports + '\n\n' +
                'Партнерские предложения по инвестированию:\n' +
                offers + '\n\n'
            ),
        },
    )

    report.context = report_context
    report.save()
