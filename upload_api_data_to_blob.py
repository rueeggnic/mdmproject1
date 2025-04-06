import os
from azure.storage.blob import BlobServiceClient

# 🔐 Connection String aus Umgebungsvariable
connect_str = os.environ.get("AZURE_STORAGE_CONNECTION_STRING")

if not connect_str:
    raise ValueError("❌ Umgebungsvariable 'AZURE_STORAGE_CONNECTION_STRING' ist nicht gesetzt!")

# 📦 Konfiguration
container_name = "apidata"  # Name deines Blob-Containers
blob_name = "stromdaten.csv"  # So heißt die Datei im Azure Blob
local_file = "data/processed/stromdaten.csv"  # Pfad zu deiner lokalen Datei

# 💡 Verbindung zu Azure Blob
blob_service_client = BlobServiceClient.from_connection_string(connect_str)
blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

# 🚀 Hochladen der Datei
with open(local_file, "rb") as data:
    blob_client.upload_blob(data, overwrite=True)

print(f"✅ Datei '{local_file}' wurde erfolgreich als '{blob_name}' in den Container '{container_name}' hochgeladen.")
