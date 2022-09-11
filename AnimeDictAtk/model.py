import typing
from pydantic import BaseModel
from pydantic.main import ModelMetaclass
import re

class AnimeFormat(BaseModel, frozen=True):
    format : str

    @classmethod
    def create(cls, base : str):
        gen = ""
        for i in base:
            if i == " ":
                gen += "0"
            else:
                gen += "1"
        return cls(format=gen)

class AnimeTitle(BaseModel):
    raw_name : str
    name : str
    raw_format : AnimeFormat
    format : AnimeFormat

    @classmethod
    def create(cls, name : str):
        raw_name = name
        # name removes all non alpha numeric characters
        name = "".join([i for i in name if i.isalnum() or i == " "])
        # removes whats in () and []
        name = re.sub("\(.*?\)", "", name)

        raw_format = AnimeFormat.create(name)
        format = AnimeFormat.create(name)
        
        return cls(raw_name=raw_name, name=name, raw_format=raw_format, format=format)
        
    def __hash__(self):
        return hash(self.name)
    
class AnimeMeta(ModelMetaclass):
    _format_mapper = {}
    _format_mapper_synonyms = {}
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        name = kwargs.get("name")
        if not name:
            raise ValueError("name is required")
    
        if name not in cls._instances:
            cls._instances[name] = super().__call__(*args, **kwargs)
            
        return cls._instances[name]
            
        

class Anime(BaseModel, metaclass=AnimeMeta):
    name : AnimeTitle
    synonyms : typing.List[AnimeTitle]

    def __init__(self, **data):
        super().__init__(**data)
        self.__class__._instances[self.name.raw_name] = self
        self.__class__._format_mapper[self.name.raw_name] = self.name.format
        for name in self.synonyms:
            self.__class__._instances[name.raw_name] = self
            self.__class__._format_mapper_synonyms[name.raw_name] = name.format
        
    
    @classmethod
    def create(cls, name : str, synonyms : typing.List[str]):
        name = AnimeTitle.create(name)
        synonyms = [AnimeTitle.create(i) for i in synonyms]
        return cls(name=name, synonyms=synonyms)

    @classmethod
    def load(cls):
        with open("AnimeDictAtk/data.json", "r", encoding="utf-8") as f:
            import json
            data = json.load(f)
            for k, v in data.items():
                cls.create(k, v)
                        
    @classmethod
    def match_format(cls, key : str):
        for k, v in cls._format_mapper.items():
            if key == v.format:
                yield k