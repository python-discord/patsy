import warnings

from sqlalchemy.exc import RemovedIn20Warning
from sqlalchemy.util import deprecations

# This needs to be set before the application is imported
# The project uses SQLAlchemy v1.4, which supports the upcoming 2.0 style
# Enabling warnings will allow a seamless transition to 2.0 once released
# See: https://docs.sqlalchemy.org/en/14/glossary.html#term-2.0-style
deprecations.SQLALCHEMY_WARN_20 = True
warnings.simplefilter("error", RemovedIn20Warning)


from patsy.main import app  # noqa: F401, E402 Unused import not at the top of the file
