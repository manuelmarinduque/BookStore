# Create your auxiliars here.

class SchemaAuxiliar:

    def GetOrCreate(self, model, name: str):
        instance, _ = model.objects.get_or_create(name=name)
        return instance


SchemaAuxiliarObj = SchemaAuxiliar()
