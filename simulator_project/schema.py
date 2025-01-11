import graphene
import kpis.schema
import simulator.schema

class Query(kpis.schema.Query, simulator.schema.Query, graphene.ObjectType):
    pass

class Mutation(kpis.schema.Mutation, simulator.schema.Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)