#!/bin/bash
# ./database/scripts/healthcheck.sh

# Check if MySQL is running and accepting connections
mysqladmin ping -h localhost --silent

# Exit with the status of the ping command
exit $?