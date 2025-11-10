import xarray as xr
import os
import glob
import zipfile

def unzip_folder(zip_path, extract_path):
    """
    Décompresse un fichier zip dans le dossier extract_path
    """
    with zipfile.ZipFile(zip_path, 'r') as zipf:
        zipf.extractall(extract_path)



# toujours utiliser multi_grib2_to_netcdf pour separer les variables en différents fichiers grib2
# et les nommer par leur noms de variables afin de contourner la limitation de grib qui n'autorise que certains noms de variables

def grib2_to_netcdf(grib2_path, ncdff_path=None):
    """
    Convertit un fichier GRIB2 (.grb2) en NetCDF (.nc) à l'aide de xarray.
    Nécessite que le moteur 'cfgrib' soit installé (ex: pip install cfgrib).
    """
        
    if ncdff_path is None:
        ncdff_path = os.path.splitext(grib2_path)[0] + "_from_grb2.nc"

    ds = xr.open_dataset(grib2_path, engine="cfgrib")
    ds.to_netcdf(ncdff_path)
    print(ds.keys())
    ds.close()

    print(f"✅ Conversion terminée : {ncdff_path}")
    return True


def multi_grib2_to_netcdf(grib2_path, ncdff_path=None, merge=False):
    """
    Convertit un fichier GRIB2 (.grb2) en NetCDF (.nc) à l'aide de xarray.
    Nécessite que le moteur 'cfgrib' soit installé (ex: pip install cfgrib).
    Si 'merge' est True, fusionne toutes les variables dans un seul fichier NetCDF
    en renommant chaque variable selon le nom du fichier GRIB2 source.
    """
        
    if ncdff_path is None:
        ncdff_path = grib2_path

    nc_filename = os.path.basename(os.path.normpath(grib2_path)).split("_")[0]

    if merge:
        l_f = glob.glob(os.path.join(grib2_path, "*.grb2"))
        datasets = []
        
        for f in l_f:
            # Extraire le nom de variable depuis le nom du fichier (sans extension)
            var_name = os.path.splitext(os.path.basename(f))[0]
            
            ds = xr.open_dataset(f, engine="cfgrib")
            
            # Renommer toutes les variables du dataset avec le nom du fichier
            old_vars = list(ds.data_vars)
            if len(old_vars) == 1:
                # Si une seule variable, renommer directement
                ds = ds.rename({old_vars[0]: var_name})
            else:
                # Si plusieurs variables, ajouter un suffixe
                rename_dict = {old_var: f"{var_name}_{old_var}" for old_var in old_vars}
                ds = ds.rename(rename_dict)
            
            datasets.append(ds)
            print(f"📂 Chargé {f} → variable(s): {list(ds.data_vars)}")
        
        # Fusionner tous les datasets
        merged_ds = xr.merge(datasets)
        output_file = os.path.join(ncdff_path, nc_filename+'.nc')
        merged_ds.to_netcdf(output_file)
        
        print(f"\n✅ Variables fusionnées: {list(merged_ds.data_vars)}")
        print(f"✅ Conversion terminée (fusionnée) : {output_file}")
        merged_ds.close()
        
    else:
        l_f = glob.glob(os.path.join(grib2_path, "*.grb2"))
        for f in l_f:
            var_name = os.path.splitext(os.path.basename(f))[0]
            
            ds = xr.open_dataset(f, engine="cfgrib")
            
            # Renommer la variable selon le nom du fichier
            old_vars = list(ds.data_vars)
            if len(old_vars) == 1:
                ds = ds.rename({old_vars[0]: var_name})
            else:
                rename_dict = {old_var: f"{var_name}_{old_var}" for old_var in old_vars}
                ds = ds.rename(rename_dict)
            
            output_file = os.path.join(ncdff_path, f"{var_name}_from_grb2.nc")
            ds.to_netcdf(output_file)
            print(f"✅ {f} → {output_file} (variable: {list(ds.data_vars)})")
            ds.close()

    return True
    

# ds.to_netcdf("/home/maxw/Documents/SATELLITE/CODES/testing/DATA_test/test_from_grb2.nc")

if __name__ == "__main__":
    # for f in glob.glob("testing/DATA_test/*.grb2"):
    #     print(f)
    unzip_folder("/home/maxw/Documents/SATELLITE/CODES/testing/DATA_test/sea/test_grib.zip", "/home/maxw/Documents/SATELLITE/CODES/testing/DATA_test/sea/test_grib")
    output_path = "/home/maxw/Documents/SATELLITE/CODES/testing/DATA_test/sea/"
    f="/home/maxw/Documents/SATELLITE/CODES/testing/DATA_test/sea/test_grib/"
    multi_grib2_to_netcdf(f, output_path, merge=True)