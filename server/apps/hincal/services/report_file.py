import io

from abc import ABC, abstractmethod
from django.conf import settings
from django.utils.timezone import now

from docxtpl import DocxTemplate
from server.apps.hincal.models import Report


class AbstractRender(ABC):  # noqa: B024
    """Абстрактный класс для рендеринга документов."""

    def __init__(self, *args, **kwargs) -> None:  # noqa: B027
        """Инициализируем переменные для работы."""
        pass

    @abstractmethod
    def render(
        self,
        context: dict,  # type: ignore
        template_full_path: str,
    ) -> io.BytesIO:
        """Рендеринг документа."""
        pass


class RenderDocx(AbstractRender):
    """Рендеринг docx-документов."""

    def render(
        self,
        context: dict,  # type: ignore
        template_full_path: str,
    ) -> io.BytesIO:
        """Рендеринг документа."""
        template = DocxTemplate(template_full_path)
        template.render(context)
        buffer = io.BytesIO()
        template.save(buffer)
        buffer.seek(0)
        return buffer


class ReportFile(object):  # noqa: WPS214
    """Генерация отчета."""

    # Рендеринг документов исходя из форматов.
    _render_handlers = {
        'docx': RenderDocx(),
        'doc': RenderDocx(),
    }

    def __init__(
        self,
        document_format: str,
        report: Report,
    ) -> None:
        """Инициализируем переменные для работы."""
        self.document_format = document_format
        self.report = report

    def get_template_full_path(self) -> str:
        """Получение шаблона для создания документа."""
        return (
            f'{settings.BASE_DIR}/server/templates/report/' +
            f'report.{self.document_format}'
        )

    def get_filename(self) -> str:
        """Получение корректного названия документа."""
        return 'Отчет_{date}.{document_format}'.format(
            date=str(now()),
            document_format=self.document_format,
        )

    def generate(self) -> io.BytesIO:
        """Генерация документа."""
        return self._render_handlers.get(self.document_format).render(
            context=self.report.context.get('context_for_file'),
            template_full_path=self.get_template_full_path(),
        )
