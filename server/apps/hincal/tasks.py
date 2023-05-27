import openai
from django.conf import settings

from server.apps.hincal.models import Report
from server.apps.hincal.services.enums import TextForReport
from server.celery import app


@app.task(bind=True)
def create_chat_gpt(self, sector: str, report_id: int) -> None:
    report = Report.objects.get(id=report_id)
    openai.api_key = settings.OPENAI_API_KEY

    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {
                'role': 'user',
                'content': (
                    "Ответ на вопрос должен состоять из нескольких предложений. Начни и закончи ответ символами '#'" +
                    f'1. Почему контроль расходов важен для промышленного предприятия в секторе {sector}?' +
                    f'2. Из каких статей состоят расходы на персонал в секторе {sector} не считая затрат на заработную плату и налоги?' +
                    f'3. Что выгоднее приобрести или арендовать землю и имущество для промышленного предприятия, которое занимается в секторе {sector}?' +
                    f'4. Какие расходы обычно забывает учитывать опытный инвестор, когда выбирает объект для инвестирования в секторе {sector}?' +
                    f'5. Какое оборудование может понадобиться предприятию, которое осуществляет свою деятельность в секторе {sector}?' +
                    f"6. Напиши пожелания для инвестора, который хочет инвестировать в предприятие, работающее в секторе {sector}. Выдели пожелание кавычками."
                )
            }
        ],
        temperature=0.7,
        top_p=1.0,
        n=1,
        max_tokens=2048,
    )
    answers = response.choices[0].message.content
    chat_gpt_page_1 = TextForReport.PAGE_1
    chat_gpt_page_2 = TextForReport.PAGE_2
    chat_gpt_page_3 = TextForReport.PAGE_3
    chat_gpt_page_4 = TextForReport.PAGE_4
    chat_gpt_page_5 = TextForReport.PAGE_5
    chat_gpt_page_6 = TextForReport.PAGE_6

    for index, answer in enumerate(answers):
        if answer == '':
            continue
        elif answer[0] == 1 or index == 1:
            chat_gpt_page_1 = answer + '\n * Сгенерировано ChatGPT'
        elif answer[0] == 2 or index == 3:
            chat_gpt_page_2 = answer + '\n * Сгенерировано ChatGPT'
        elif answer[0] == 3 or index == 5:
            chat_gpt_page_3 = answer + '\n * Сгенерировано ChatGPT'
        elif answer[0] == 4 or index == 7:
            chat_gpt_page_4 = answer + '\n * Сгенерировано ChatGPT'
        elif answer[0] == 5 or index == 9:
            chat_gpt_page_5 = answer + '\n * Сгенерировано ChatGPT'
        elif answer[0] == 6 or index == 11:
            chat_gpt_page_6 = 'Пожелание от ChatGPT: ' + answer[2:-1]

    report_context = report.context
    report_context.get('context_for_file').update(
        {
            'chat_gpt_page_1': chat_gpt_page_1,
            'chat_gpt_page_2': chat_gpt_page_2,
            'chat_gpt_page_3': chat_gpt_page_3,
            'chat_gpt_page_4': chat_gpt_page_4,
            'chat_gpt_page_5': chat_gpt_page_5,
            'chat_gpt_page_6': chat_gpt_page_6,
        }
    )

    report.context = report_context
    report.context.save()
