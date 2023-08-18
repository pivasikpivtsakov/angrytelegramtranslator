import json

from pydantic import BaseModel


class FormDataModel(BaseModel):
    def as_form_data_dict(self):
        d = self.dict().items()
        return {
            key: val if type(val) is str else json.dumps(val)
            for key, val in d
            if val is not None and key is not None
        }
