python $(pwd)/main.py
python $(pwd)/etat_annonces.py
read -p "ouvrir navigateur ou telecharger annonces ? O/n" rep

if [ "${rep}" == "O" ]; then
    python $(pwd)/annonces.py
    read -p "presser entree une fois les annonces telechargees" rep
    python $(pwd)/etat_annonces.py
fi
python $(pwd)/extract_items.py
python $(pwd)/enrich_items.py

cp items.json ../django_projects/rechercheMaison/data/maisons.json
cd ../django_projects/rechercheMaison
python manage.py runscript import_maisons
cd -
./sauvegarde.sh