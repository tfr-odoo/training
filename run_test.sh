#! /bin/bash
export LOAD_TEST=test_create_course,test_course_unique
echo $LOAD_TEST
createdb academy_test
coverage run --branch /home/odoo/odoo/odoo.py  --addons-path=../odoo/addons,. -i academy -d academy_test --test-enable --log-level=test --stop-after-init
dropdb academy_test
coverage report --include=./academy/*  -m
rm .coverage
