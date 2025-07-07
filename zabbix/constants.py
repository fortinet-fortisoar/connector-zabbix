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
SEVERITY_MAP = {"Not classified": "0", "Information": "1", "Warning": "2", "Average": "3", "High": "4", "Disaster": "5"
                }
ALERTS_PAYLOAD = {"jsonrpc": "2.0", "method": "alert.get", "params": {}, "id": 1}
EVENTS_PAYLOAD = {"jsonrpc": "2.0", "method": "event.get", "params": {}, "id": 1}
PROBLEMS_PAYLOAD = {"jsonrpc": "2.0", "method": "problem.get", "params": {}, "id": 1
                    }
DEFAULT_RESPONSE = {"status": "success", "message": "No record found for this RPC request"}
BASIC_AUTH = 'Basic Auth'
CLIENT_CRED = 'Client Credentials'
AUTH_REQUEST_BODY = {"jsonrpc": "2.0", "method": "user.login", "params": {}, "id": 1}
