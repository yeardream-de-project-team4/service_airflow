#!/bin/bash

# initialize database
airflow db init

# user create
airflow users create \
	--username ${AIRFLOW_USERNAME} \
	--password ${AIRFLOW_PASSWORD} \
	--firstname ${AIRFLOW_FIRSTNAME} \
	--lastname ${AIRFLOW_LASTNAME} \
	--role ${AIRFLOW_ROLE} \
	--email ${AIRFLOW_EMAIL}