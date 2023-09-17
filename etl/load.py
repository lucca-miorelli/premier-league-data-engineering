################################################################################
##                                  LIBRARIES                                 ##
################################################################################

################
##  EXTERNAL  ##
################

import contextlib
from sqlalchemy import create_engine, text


################################################################################
##                                  FUNCTIONS                                 ##
################################################################################


def get_db_engine(postgresql_url: str = None):
    """
    Create a new database engine and yield it to the caller.

    Returns
    -------
    Engine
        A SQLAlchemy Engine object representing a database engine.
    """
    if postgresql_url is None:
        raise ValueError("The postgresql_url parameter cannot be None.")
    engine = create_engine(postgresql_url)
    return engine
