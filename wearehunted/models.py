from jsonmodels import Model, Field, DictField

class ArtistChartEntry(Model):
  artist_id = Field()
  artist    = Field()
  links     = DictField()

class SingleChartEntry(Model):
  track     = Field()
  artist_id = Field()
  artist    = Field()
  links     = DictField()