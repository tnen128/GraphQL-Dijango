import graphene
from graphene_django import DjangoObjectType
from .models import KPI

class KPIType(DjangoObjectType):
    class Meta:
        model = KPI
        fields = ('id', 'formula')

class CreateKPI(graphene.Mutation):
    class Arguments:
        formula = graphene.String(required=True)

    kpi = graphene.Field(KPIType)

    def mutate(self, info, formula):
        kpi = KPI.objects.create(formula=formula)
        return CreateKPI(kpi=kpi)

class UpdateKPI(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        formula = graphene.String(required=True)

    kpi = graphene.Field(KPIType)

    def mutate(self, info, id, formula):
        try:
            kpi = KPI.objects.get(pk=id)
            kpi.formula = formula
            kpi.save()
            return UpdateKPI(kpi=kpi)
        except KPI.DoesNotExist:
            raise Exception('KPI not found')

class DeleteKPI(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        try:
            kpi = KPI.objects.get(pk=id)
            kpi.delete()
            return DeleteKPI(success=True)
        except KPI.DoesNotExist:
            return DeleteKPI(success=False)

class Query(graphene.ObjectType):
    kpis = graphene.List(KPIType)
    kpi = graphene.Field(KPIType, id=graphene.Int())
    calculate_kpi = graphene.Float(kpi_id=graphene.Int(), value=graphene.Float())

    def resolve_kpis(self, info):
        return KPI.objects.all()

    def resolve_kpi(self, info, id):
        try:
            return KPI.objects.get(id=id)
        except KPI.DoesNotExist:
            return None

    def resolve_calculate_kpi(self, info, kpi_id, value):
        try:
            kpi = KPI.objects.get(id=kpi_id)
            return kpi.apply_formula(value)
        except KPI.DoesNotExist:
            raise Exception('KPI not found')

class Mutation(graphene.ObjectType):
    create_kpi = CreateKPI.Field()
    update_kpi = UpdateKPI.Field()
    delete_kpi = DeleteKPI.Field()