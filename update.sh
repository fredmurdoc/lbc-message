python $(pwd)/main.py
python $(pwd)/extract_items.py
python $(pwd)/enrich_items.py
cp items.json ../django_projects/rechercheMaison/data/maisons.json
cd ../django_projects/rechercheMaison
python manage.py runscript import_maisons