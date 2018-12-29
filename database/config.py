ENV = "DEV"

assert ENV == "DEV" or ENV == "TEST", "Unknown environment."
if ENV == "DEV":
    USER = "postgres"
    NAME = "charlotte"
    PASSWORD = "DATABASE SECRET HERE"
    PORT = 5432
elif ENV == "TEST":
    USER = "postgres"
    NAME = "charlotte_test"
    PASSWORD = "DATABASE SECRET HERE"
    PORT = 5432
