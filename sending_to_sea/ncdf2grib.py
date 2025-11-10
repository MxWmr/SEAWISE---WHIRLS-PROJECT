import subprocess
import os
import glob

import xarray as xr
import subprocess
import os
import zipfile

def convert_nc_variables_to_grib2_cdo(nc_path, output_dir=None):

    """
    Convertit chaque variable d'un NetCDF en fichier GRIB2 séparé via CDO.
    """
    ds = xr.open_dataset(nc_path)
    variables = [v for v in ds.data_vars]

    if not variables:
        raise ValueError(f"Aucune variable trouvée dans {nc_path}")

    if output_dir is None:
        output_dir = os.path.splitext(nc_path)[0] + "_grib"
    os.makedirs(output_dir, exist_ok=True)

    print(f"📦 Conversion des variables du NetCDF : {nc_path}")
    print(f"📁 Fichiers GRIB2 enregistrés dans : {output_dir}\n")

    for var in variables:
        grib_path = os.path.join(output_dir, f"{var}.grb2")

        # Approche 1 : Utiliser -selname au lieu de -select,name=
        cmd = [
            "cdo", "-f", "grb2", "copy", "-selname," + var,
            nc_path, grib_path
        ]


        print(f"➡️  Conversion de '{var}' → {os.path.basename(grib_path)}")
        try:
            subprocess.run(cmd, check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ Erreur avec -selname: {e.stderr.decode('utf-8')}")
        else:
            print(f"✅ {var} → {grib_path}")




def zip_folder(folder_path, zip_path):
    """
    Compresse un dossier (folder_path) en un fichier zip (zip_path)
    """
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                # Chemin relatif pour éviter d'inclure le chemin complet
                arcname = os.path.relpath(file_path, start=folder_path)
                zipf.write(file_path, arcname)




if __name__ == "__main__":
    f = "/home/maxw/Documents/SATELLITE/CODES/testing/DATA_test/land/test.nc"
    convert_nc_variables_to_grib2_cdo(f)
    repo_to_zip = "/home/maxw/Documents/SATELLITE/CODES/testing/DATA_test/land/test_grib"
    zipped_repo = repo_to_zip+".zip"
    zip_folder(repo_to_zip,zipped_repo)
