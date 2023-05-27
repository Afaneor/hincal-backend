from server.apps.hincal.models import Report


def add_offers_and_wishes_in_context(
    report: Report,
    data: dict,
):
    """Формирование предложений и мер поддержки."""
    report_context = report.context

    if report_context.get('context_for_file').get('offers_and_wishes'):
        return None
    areas = ''
    supports = ''
    offers = ''
    for key_dict, value_dict in data.items():
        if key_dict == 'areas':
            for index, area in enumerate(value_dict[0:1]):
                areas += (
                    f'Площадка № {index}:\n' +
                    f'Название: {area.title}\n' +
                    f'Адрес: {area.address}\n' +
                    f'Подробнее: {area.site}\n'
                )

        if key_dict == 'supports':
            for index, support in enumerate(value_dict[0:1]):
                supports += (
                    f'Мера поддержки № {index}:\n' +
                    f'Название: {support.title}\n' +
                    f'Описание: {support.text}\n' +
                    f'Сумма субсидий: {support.amount}\n' +
                    f'Подробнее: {support.site}\n'
                )

        if key_dict == 'offers':
            for index,offer in enumerate(value_dict[0:1]):
                offers += (
                    f'Партнерское предложение № {index}:\n' +
                    f'Название: {offer.title}\n' +
                    f'Процентная ставка: {offer.interest_rate}\n' +
                    f'Срок займа{offer.loan_term}\n' +
                    f'amount{offer.amount}\n' +
                    f'Подробнее: {offer.site}\n'
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
            )
        }
    )

    report.context = report_context
    report.context.save()
