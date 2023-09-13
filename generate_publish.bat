python .\generator\make.py ..\published\

cd ..\published\
git add *
git commit -m "published"
git push origin HEAD:published