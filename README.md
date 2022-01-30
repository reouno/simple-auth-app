# Requirements
- python3.9
- pip

# Install
#### 1. clone this repo

#### 2. Execute the following commands
```shell
# Under the projcet root
cd api_server

# install python packages
pip install -r requirements.txt

# migration
python manage.py migrate
# --> db.sqlite3 will be created

# create super user
python manage.py createsuperuser
# --> Visible user id: TYPE ID IN EMAIL ADDESS FORMAT!!
# --> Password: set password
```

# Run in local environment
```shell
# Under the project root
cd api_server

# Run django api server
python manage.py runserver
```

# Deploy to Cloud Run
#### 1. Create resources
You have to create resources in GCP.

Instruction: https://cloud.google.com/python/django/run

#### 2. Edit files
You have to change values in `api_server/cloudmigrate.yaml` and `api_server/deploy-cloud-run.yaml` according to your GCP environment.

#### 3. First deployment
Please follow the instruction in the above link.

#### 4. Update
```shell
# Under the project root
cd api_server

./deploy-cloud-run.sh
```