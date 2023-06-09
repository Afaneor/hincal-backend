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
                    f'Площадка № {en_index}:\r\n' +
                    f"Название: {area.get('title')}\r\n" +
                    f"Адрес: {area.get('address')}\r\n" +
                    f"Подробнее: {area.get('site')}\r\n"
                )

        if key_dict == 'supports':
            for en_index, support in enumerate(value_dict[0:1]):  # noqa: WPS440
                supports += (
                    f'Мера поддержки № {en_index}:\r\n' +
                    f"Название: {support.get('title')}\r\n" +
                    f"Описание: {support.get('text')}\r\n" +
                    f"Сумма субсидий: {support.get('amount')}\r\n" +
                    f"Подробнее: {support.get('site')}\r\n"
                )

        if key_dict == 'offers':
            for en_index, offer in enumerate(value_dict[:1]):  # noqa: WPS440
                offers += (
                    f'Партнерское предложение № {en_index}:\r\n' +
                    f"Название: {offer.get('title')}\r\n" +
                    f"Процентная ставка: {offer.get('interest_rate')}\r\n" +
                    f"Срок займа{offer.get('loan_term')}\r\n" +
                    f"amount{offer.get('amount')}\r\n" +
                    f"Подробнее: {offer.get('site')}\r\n"
                )

    report_context.get('context_for_file').update(
        {
            'offers_and_wishes': (
                'Площадки для создания промышленного предприятия:\r\n' +
                areas + '\r\n\r\n' +
                'Меры по поддержке промышленных предприятий:\r\n' +
                supports + '\r\n\r\n' +
                'Партнерские предложения по инвестированию:\r\n' +
                offers + '\r\n\r\n'
            ),
        },
    )

    report.context = report_context
    report.save()
