import graphene
from graphene_django import DjangoObjectType
from parking.models import ParkingSpot

class ParkingType(DjangoObjectType):
    class Meta:
        model = ParkingSpot
        fields = ('sensor_id', 'sensor_status', 'sensor_location', 'sensor_type' )
        
# REGISTRA UN SENSOR
class CreateSpot(graphene.Mutation):
    class Arguments:
        sensor_id = graphene.String()
        sensor_status = graphene.Boolean()
        sensor_location = graphene.String()
        sensor_type = graphene.String()
        
    spot = graphene.Field(ParkingType)
    
    def mutate(self, info, sensor_id, sensor_status, sensor_location, sensor_type):
        spot = ParkingSpot(sensor_id=sensor_id, sensor_status=sensor_status, sensor_location=sensor_location, sensor_type=sensor_type)
        spot.save()
        return CreateSpot(spot)

# ELIMINA UN SPOT
class DeleteSpot(graphene.Mutation):
    class Arguments:
        sensor_id = graphene.String()
        
    ok = graphene.Boolean()
    
    def mutate(self, info, sensor_id):
        spot = ParkingSpot.objects.get(sensor_id=sensor_id)
        spot.delete()
        return DeleteSpot(ok=True)

# ACTUALIZA EL SPOT
class UpdateSpot(graphene.Mutation):
    class Arguments:
        sensor_id = graphene.String()
        sensor_status = graphene.Boolean()
        
    spot = graphene.Field(ParkingType)
    
    def mutate(self, info, sensor_id, sensor_status):
        spot = ParkingSpot.objects.get(sensor_id=sensor_id)
        spot.sensor_status = sensor_status
        spot.save()
        return UpdateSpot(spot)

# MÉTODOS GET O EQUIVALENTE
class Query(graphene.ObjectType):
    hello = graphene.String(name=graphene.String(default_value="stranger"))
    spots = graphene.List(ParkingType)
    spot = graphene.Field(ParkingType, sensor_id=graphene.ID())

    def resolve_hello(self, info, name):
        return f"Hello {name}"
      
    def resolve_spots(self, info):
        return ParkingSpot.objects.all()
      
    def resolve_spot(self, info, sensor_id):
        return ParkingSpot.objects.get(sensor_id=sensor_id)
      
# MUTACIONES (POST, PUT, DELETE) O EQUIVALENTE
class Mutation(graphene.ObjectType):
  create_spot = CreateSpot.Field() # REGISTRAR EL DATO EQUIVALENTE AL POST
  delete_spot = DeleteSpot.Field() # ELIMINAR EL DATO EQUIVALENTE AL DELETE
  update_spot = UpdateSpot.Field() # ACTUALIZAR EL DATO EQUIVALENTE AL PUT O AL PATCH
  
schema = graphene.Schema(query=Query, mutation=Mutation)