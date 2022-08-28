import graphene
from graphene import ObjectType,String,Schema,relay,Int
from graphene_sqlalchemy import SQLAlchemyObjectType,SQLAlchemyConnectionField
from .models import Project as ProjectModel,Therb as TherbModel,db_session

class Project(SQLAlchemyObjectType):
    class Meta:
        model = ProjectModel
        interfaces = (relay.Node,)

# class Result(SQLAlchemyObjectType):
#     class Meta:
#         model = ResultModel
#         interfaces = (relay.Node,)
class Therb(SQLAlchemyObjectType):
    class Meta:
        model = TherbModel
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
    #project = graphene.List(Project,q=String())
    result = graphene.List(Therb,q=Int())
    #all_projects = SQLAlchemyConnectionField(Project.connection)
    #all_results = SQLAlchemyConnectionField(Result.connection)

    def resolve_project(self,info,**args):
        q = args.get('q')

        project_query = ProjectModel.query.filter(ProjectModel.name.contains(q)).all()

        return project_query

    def resolve_result(self,info,**args):
        q = args.get('q')
        result_query = TherbModel.query.filter(TherbModel.project_id==q)

        return result_query

class Mutation(ObjectType):
    insert_project = InsertProject.Field()

schema = Schema(query=Query,mutation=Mutation)


