import logging
from pymodm import MongoModel, fields, connect

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

connect("mongodb://mongo/talosdb")

class Competition(MongoModel):

    name = fields.CharField(required=True)
    created_at = fields.DateTimeField(required=True)
    deadline = fields.DateTimeField()
    url = fields.URLField()
