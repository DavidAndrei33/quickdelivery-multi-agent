# QuickDelivery - Database Initialization
# This script runs when PostgreSQL container starts for the first time
# It creates the initial database structure

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create schema if not exists
CREATE SCHEMA IF NOT EXISTS public;

-- Set timezone
SET timezone = 'UTC';

-- Add comment for logging
COMMENT ON DATABASE quickdelivery IS 'QuickDelivery Food Platform Database';
