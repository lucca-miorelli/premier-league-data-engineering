################################################################################
##                                  LIBRARIES                                 ##
################################################################################

################
##  EXTERNAL  ##
################

import os


################################################################################
##              ENVIRONMENT VARIABLES, CONFIGURATIONS, & SETTINGS             ##
################################################################################

# Set the BASE_URL 
BASE_URL = "https://apiv3.apifootball.com/"

# Set the DATE_RANGES
DATE_RANGES = [
    {"from": "2022-08-01", "to": "2022-11-11"},
    {"from": "2022-11-12", "to": "2023-05-29"}
]

# Set the API_KEY
# The API_KEY is an environment variable that should be set externally, either
# in the local environment or within a Docker container, depending on where
# this code is running.
API_KEY = os.environ["API_KEY"]

# Set the BASE_PAYLOAD
BASE_PAYLOAD =  {
    "action": "get_events",
    "league_id": "152",
    "APIkey": API_KEY
}

# Set the POSTGRESQL_URL
# The POSTGRESQL_URL is constructed using environment variables for database
# connection. Ensure that these environment variables are set appropriately
# in the respective environment, whether it's the local development environment
# or a Docker container environment.
POSTGRESQL_URL = (
    f"postgresql://"
    f"{os.environ['POSTGRES_USER']}"
    f":{os.environ['POSTGRES_PASSWORD']}@"
    f"premier-league-postgres:5432/"
    f"{os.environ['POSTGRES_DB']}"
)
