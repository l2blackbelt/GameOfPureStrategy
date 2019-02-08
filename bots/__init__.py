#grab all the bot files and import them
from os.path import dirname, basename, isfile
import glob
bot_files = glob.glob(dirname(__file__)+"/*.py")
__all__ = [ basename(f)[:-3] for f in bot_files if isfile(f) and not f.endswith('__init__.py')]
#print(__all__)