""""
Copyright start
MIT License
Copyright (c) 2025 Fortinet Inc
Copyright end
"""
ERROR_MSG = {
            400: 'Bad/Invalid Request',
            401: 'Unauthorized: Invalid credentials or token provided failed to authorize',
            403: 'Forbidden, source data source is read-only',
            404: 'Not found, either source or target data source could not be found',
            500: 'Internal Server Error',
            503: 'Service Unavailable',
            'time_out': 'The request timed out while trying to connect to the remote server',
            'ssl_error': 'SSL certificate validation failed'
        }

EVENT_OBJECT_TYPE_MAP = {
    "Trigger": 0,
    "Discovered Host": 1,
    "Discovered Service": 2,
    "Auto-Registered Host": 3,
    "Item": 4,
    "LLD Rule": 5,
    "Service": 6
}

EVENT_SOURCE_MAP = {
    "Event Created by a Trigger": 0,
    "Event Created by a Discovery Rule": 1,
    "Event Created by Active Agent Auto Registration": 2,
    "Internal Event": 3,
    "Event Created on Service Status Update": 4
}
