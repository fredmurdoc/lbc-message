python $(pwd)/main.py

if [ ! -f items.json ]; then
    echo "bdd vide, recreation"
    python $(pwd)/extract_items.py
fi

python $(pwd)/extract_items.py
python $(pwd)/etat_annonces.py
read -p "ouvrir navigateur ou telecharger annonces ? O/n" rep

if [ "${rep}" == "O" ]; then
    python $(pwd)/annonces.py
    read -p "presser entree une fois les annonces telechargees" rep
    python $(pwd)/etat_annonces.py
fi

python $(pwd)/enrich_items.py > $(pwd)/enrich_items.log
echo "Copie des items vers le project Django et import"
cp items.json ../django_projects/rechercheMaison/data/annonces.json
