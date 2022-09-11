from AnimeDictAtk.model import Anime, AnimeMeta
import zipfile
def load():
    # unzip the data.zip
    with zipfile.ZipFile("AnimeDictAtk/data.zip", "r") as zip_ref:
        zip_ref.extractall("AnimeDictAtk")
    Anime.load()
