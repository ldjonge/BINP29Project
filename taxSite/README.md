## This web-based application was created using Django and searches a database for information on the specified taxon
To run this application the following steps need to be performed

# Django
Django is a package for python3 that must be installed on the system before this application can be run. With python installed, this can be done on the entire system using "pip -m install django". This installs the latest version automatically. Alternatively it can be installed in a virtual environment, for example using Anaconda. This project was created using Django version 2.1.7. For more information visit https://djangoproject.com

# Downloading the data
The data was retrieved from the European Bioinformatics Institute. To download the data use "wget ftp://ftp.ebi.ac.uk/pub/databases/taxonomy/taxonomy.dat" in the main directory of this project.

# Creating the SQL database
To set up the initial database structure, run the following commands in the main project directory:  
python3 manage.py makemigrations  
python3 manage.py migrate  
Then to enter the downloaded data into this database run the following command:  
python3 createTaxDb.py taxonomy.dat  

# Running the application
To access the web application it must first be activated using the following command:  
python3 manage.py runserver  
This command will return the address at which the application can be found. Navigating to this address will give access to the application
