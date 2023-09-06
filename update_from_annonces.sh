python $(pwd)/extract_annonces_from_dir.py

echo "Copie des items vers le project Django et import"
cp items.json ../django_projects/rechercheMaison/data/annonces.json
cd ../django_projects/rechercheMaison
./update.sh
cd -
echo "sauvegarde des annonces"
./sauvegarde.sh