import graphene
from graphene import ObjectType,String,Schema,relay
from graphene_sqlalchemy import SQLAlchemyObjectType,SQLAlchemyConnectionField
from .models import Project as ProjectModel,Results as ResultModel,db_session

class Project(SQLAlchemyObjectType):
    class Meta:
        model = ProjectModel
        interfaces = (relay.Node,)

class Result(SQLAlchemyObjectType):
    class Meta:
        model = ResultModel
        interfaces = (relay.Node,)

class InsertProject(graphene.Mutation):
    class Arguments:
        name = String(required=True)

    project = graphene.Field(lambda: Project)
    
    def mutate(self,info,name):
        project = ProjectModel(name=name)
        
        db_session.add(project)
        db_session.commit()

        return InsertProject(project=project)

class Query(ObjectType):
    node = relay.Node.Field()
    all_projects = SQLAlchemyConnectionField(Project.connection)
    all_results = SQLAlchemyConnectionField(Result.connection)

class Mutation(ObjectType):
    insert_project = InsertProject.Field()

schema = Schema(query=Query,mutation=Mutation)

# class Query(ObjectType):
#     hello = String(name=String(default_value="stranger"))

#     def resolve_hello(self, info, name):
#         return "Hello " + name

# schema = Schema(query=Query)

