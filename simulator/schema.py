import graphene
from graphene_django import DjangoObjectType
from .models import Simulator

class SimulatorType(DjangoObjectType):
    class Meta:
        model = Simulator
        fields = ('id', 'start_date', 'interval', 'kpi_id')

class CreateSimulator(graphene.Mutation):
    class Arguments:
        start_date = graphene.DateTime(required=True)
        interval = graphene.Int(required=True)
        kpi_id = graphene.ID(required=True)

    simulator = graphene.Field(SimulatorType)

    def mutate(self, info, start_date, interval, kpi_id):
        simulator = Simulator.objects.create(
            start_date=start_date,
            interval=interval,
            kpi_id_id=kpi_id
        )
        return CreateSimulator(simulator=simulator)

class UpdateSimulator(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        start_date = graphene.DateTime()
        interval = graphene.Int()
        kpi_id = graphene.ID()

    simulator = graphene.Field(SimulatorType)

    def mutate(self, info, id, **kwargs):
        try:
            simulator = Simulator.objects.get(pk=id)
            for key, value in kwargs.items():
                if key == 'kpi_id':
                    setattr(simulator, 'kpi_id_id', value)
                else:
                    setattr(simulator, key, value)
            simulator.save()
            return UpdateSimulator(simulator=simulator)
        except Simulator.DoesNotExist:
            raise Exception('Simulator not found')

class DeleteSimulator(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        try:
            simulator = Simulator.objects.get(pk=id)
            simulator.delete()
            return DeleteSimulator(success=True)
        except Simulator.DoesNotExist:
            return DeleteSimulator(success=False)

class Query(graphene.ObjectType):
    simulators = graphene.List(SimulatorType)
    simulator = graphene.Field(SimulatorType, id=graphene.Int())

    def resolve_simulators(self, info):
        return Simulator.objects.all()

    def resolve_simulator(self, info, id):
        try:
            return Simulator.objects.get(id=id)
        except Simulator.DoesNotExist:
            return None

class Mutation(graphene.ObjectType):
    create_simulator = CreateSimulator.Field()
    update_simulator = UpdateSimulator.Field()
    delete_simulator = DeleteSimulator.Field()