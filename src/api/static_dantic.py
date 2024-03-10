import pydantic
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from apiguy import *


def create_model(model_name, model_def):
    fields = {
        field_name: pydantic.Field(**field_def) 
        for field_name, field_def in model_def.items()
    }
    return pydantic.create_model(model_name, **fields) 