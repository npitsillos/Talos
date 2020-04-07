import logging
from pymodm import MongoModel, fields, connect

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

connect("mongodb://data/talosdb")

class Competition(MongoModel):

    name = fields.CharField(required=True)
    # created_at = fields.DateTimeField()
    # deadline = fields.DateTimeField()
    # url = fields.URLField()
