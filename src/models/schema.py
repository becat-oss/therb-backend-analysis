import graphene
from graphene import ObjectType,String,Schema,relay
from graphene_sqlalchemy import SQLAlchemyObjectType,SQLAlchemyConnectionField
from .models import db_session, Project as ProjectModel,Results as ResultModel

class Project(SQLAlchemyObjectType):
    class Meta:
        model = ProjectModel
        interfaces = (relay.Node,)

class Result(SQLAlchemyObjectType):
    class Meta:
        model = ResultModel
        interfaces = (relay.Node,)

class Query(ObjectType):
    node = relay.Node.Field()
    all_projects = SQLAlchemyConnectionField(Project.connection)
    all_results = SQLAlchemyConnectionField(Result.connection)

schema = Schema(query=Query)

# class Query(ObjectType):
#     hello = String(name=String(default_value="stranger"))

#     def resolve_hello(self, info, name):
#         return "Hello " + name

# schema = Schema(query=Query)

