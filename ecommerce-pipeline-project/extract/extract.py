import pandas as pd
import os

# Chemin vers le dossier data (un niveau au-dessus du dossier extract)
data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')

# Vérifier si le dossier existe
if not os.path.exists(data_dir):
    raise FileNotFoundError(f"Le dossier {data_dir} n'existe pas. Veuillez créer le dossier 'data' dans le répertoire principal du projet.")

summary = []

for file in os.listdir(data_dir):
    if file.endswith('.csv'):
        path = os.path.join(data_dir, file)
         
        try:
            df = pd.read_csv(path)
            summary.append({
                'file_name': file,
                'num_rows': len(df),
                'num_columns': len(df.columns)
            })
        except Exception as e:
            summary.append({
                'file_name': file,
                'error': str(e)
            })

# Créer un DataFrame à partir de la liste summary
df_summary = pd.DataFrame(summary)

# Afficher le tableau avec un formatage amélioré
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
print("\nRésumé des fichiers CSV :")
print(df_summary.to_string(index=False))