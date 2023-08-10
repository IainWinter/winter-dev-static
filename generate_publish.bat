python .\generator\main.py ..\published\

cdc ..\published\
git add *
git commit -m "published"
git push origin HEAD:published

PAUSE