from server.apps.hincal.models import Archive
from server.apps.services.serializers import ModelSerializerWithPermission


class ArchiveSerializer(ModelSerializerWithPermission):
    """Сериалайзер архива."""

    class Meta(object):
        model = Archive
        fields = (
            'id',
            'year',
            'income_tax_rate_to_the_subject_budget',
            'income_tax_rate_to_the_federal_budget',
            'land_tax_rate',
            'property_tax_rate',
            'patent_tax_rate',
            'personal_income_rate',
            'pension_contributions_rate',
            'medical_contributions_rate',
            'lower_tax_margin_error',
            'upper_tax_margin_error',
            'cost_accounting',
            'registration_costs',
            'is_actual',
            'permission_rules',
            'created_at',
            'updated_at',
        )


class ArchiveForReportSerializer(ModelSerializerWithPermission):
    """Сериалайзер архива для контекста."""

    class Meta(object):
        model = Archive
        fields = (
            'year',
            'income_tax_rate_to_the_subject_budget',
            'income_tax_rate_to_the_federal_budget',
            'land_tax_rate',
            'property_tax_rate',
            'patent_tax_rate',
            'personal_income_rate',
            'pension_contributions_rate',
            'medical_contributions_rate',
            'lower_tax_margin_error',
            'upper_tax_margin_error',
            'cost_accounting',
            'registration_costs',
        )
