#!/bin/sh
echo "Running docker-install.sh..."

echo "Running flask db seed commands...this takes a while, please be patient..."
flask db upgrade
flask seed_test_db
flask update_pipeline_data
flask seed_test_experiments

# Start the actual web server
echo "Starting the Flask web server..."
exec flask run --host=0.0.0.0 --port=4000
