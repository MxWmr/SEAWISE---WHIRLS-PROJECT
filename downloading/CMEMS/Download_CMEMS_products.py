import copernicusmarine
from datetime import datetime
import copernicusmarine
from datetime import datetime
import os
from dotenv import load_dotenv
from pathlib import Path

# Charger les identifiants depuis un fichier .env
dotenv_path = Path('credentials_CMEMS.env')
load_dotenv(dotenv_path=dotenv_path)

USERNAME = os.getenv("MAIL")
PASSWORD = os.getenv("PASSWORD")
print(USERNAME)
print(PASSWORD)



copernicusmarine.subset(
    username=USERNAME,
    password=PASSWORD,
    dataset_id="cmems_mod_glo_phy_my_0.083deg_P1D-m",
    variables=["uo", "vo"],
    output_directory=".",
    output_filename="test.nc",
    minimum_longitude=6.5,
    maximum_longitude=27,
    minimum_latitude=-44,
    maximum_latitude=-29,
    start_datetime=datetime(2010, 1, 1),
    end_datetime=datetime(2010, 1, 4),
    disable_progress_bar=True,
    minimum_depth=0,
    maximum_depth=5
) 