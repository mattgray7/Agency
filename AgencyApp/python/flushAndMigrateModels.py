import os

# Flush
os.system("python /Users/MattGray/Projects/Agency/Agency/manage.py flush")

os.system("python /Users/MattGray/Projects/Agency/Agency/manage.py makemigrations")
os.system("python /Users/MattGray/Projects/Agency/Agency/manage.py migrate")

os.system("python -c 'from django.conf import settings;"
		              "settings.configure();"
					  "import models;"
					  "import constants;"
					  "for profession in constants.PROFESSIONS:;"
					  "    p = models.Profession(name=profession);"
					  "    p.save()';")

""")from django.conf import settings
settings.configure()
import AgencyApp.python.models as models
import AgencyApp.python.constants as constants
print "Adding professions to db"
for profession in constants.PROFESSIONS:
    p = models.MasterProfession(professionName=profession)
    p.save()"""
