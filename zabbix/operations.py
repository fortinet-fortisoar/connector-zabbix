"""""
Copyright start
MIT License
Copyright (c) 2025 Fortinet Inc
Copyright end
"""

import json
from datetime import datetime

import requests
from connectors.core.connector import get_logger, ConnectorError

from .constants import EVENT_OBJECT_TYPE_MAP, EVENT_SOURCE_MAP, ERROR_MSG

logger = get_logger('zabbix')


class Zabbix(object):
    def __init__(self, config):
        self.server_url = config.get('server_url', '').strip('/')
        if not self.server_url.startswith('https://') and not self.server_url.startswith('http://'):
            self.server_url = 'https://' + self.server_url
        self.api_key = config.get('api_key')
        self.verify_ssl = config.get('verify_ssl')
        self.headers = {
            'Authorization': 'Bearer {}'.format(self.api_key),
            'Content-Type': 'application/json'
        }
        self.endpoint = 'api_jsonrpc.php'


    def make_api_call(self, method='post', payload=None, params=None):
        try:
            service_endpoint = f'{self.server_url}/{self.endpoint}'
            logger.debug("service_endpoint : {}".format(service_endpoint))
            logger.debug("Rest API Payload : {}".format(payload))
            response = requests.request(method, service_endpoint, headers=self.headers, params=params, data=payload,
                                        verify=self.verify_ssl)
            logger.debug("Rest API Response Status code : {}".format(response.status_code))
            if response.ok:
                json_resp = response.json()
                result = json_resp.get('result')
                if result == [] or result:
                    return json_resp
                else:
                    raise ConnectorError(json_resp)
            else:
                logger.error(f'{ERROR_MSG.get(response.status_code)}: {response.text}')
                raise ConnectorError({'status': 'Failure', 'status_code': str(response.status_code),
                'response': '{}: {}'.format(self.error_msg.get(response.status_code), response.text)})
        except requests.exceptions.SSLError as err:
            logger.error(err)
            raise ConnectorError('SSL certificate validation failed')
        except requests.exceptions.ConnectTimeout as err:
            logger.error(err)
            raise ConnectorError('The request timed out while trying to connect to the server')
        except requests.exceptions.ReadTimeout as err:
            logger.error(err)
            raise ConnectorError('The server did not send any data in the allotted amount of time')
        except requests.exceptions.ConnectionError as err:
            logger.error(err)
            raise ConnectorError('Invalid endpoint or credentials')
        except Exception as err:
            logger.error(err)
            raise ConnectorError(str(err))


def get_datime_to_timestamp(datetime_str):
    dt_obj = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    return int(dt_obj.timestamp())


def get_string_to_list(input_parameters):
    if isinstance(input_parameters, str):
        input_parameters = input_parameters.split(',')
    if isinstance(input_parameters, list):
        input_parameters = [x.strip() for x in input_parameters]
    return input_parameters


def parse_to_dict(raw_text):
    lines = raw_text.strip().split('\n')
    result = {}
    for line in lines:
        if not line.strip():
            continue
        if ": " in line:
            key, value = line.split(": ", 1)
            result[key.strip().lower().replace(' ', '_')] = value.strip()
        else:
            pass
    return result


def parse_response(resp):
    try:
        result = resp.get('result')
        for item in result:
            message = item.get('message', '')
            json_data = parse_to_dict(message)
            item.update(json_data)
        return resp
    except Exception as err:
        logger.warning("Parsing Failed: {}".format(err))
        return resp


def build_rpc_request_payload(params, payload):
    params = {k: v for k, v in params.items() if v is not None and v != ''}
    start_date = params.get('start_date')
    # payload['']=''
    if start_date:
        payload.get('params', {}).update({'time_from': get_datime_to_timestamp(start_date)})
    end_date = params.get('end_date')
    if end_date:
        payload.get('params', {}).update({'time_till': get_datime_to_timestamp(end_date)})
    filter_string = params.get('filter')
    if filter_string:
        payload.get('params', {}).update({'filter': filter_string})
    search = params.get('search')
    if search:
        payload.get('params', {}).update({'search': search})
    search_any = params.get('search_any')
    if search_any:
        payload.get('params', {}).update({'searchByAny': search_any})
    search_wildcards_enabled = params.get('search_wildcards_enabled')
    if search_wildcards_enabled:
        payload.get('params', {}).update({'searchWildcardsEnabled': search_wildcards_enabled})
    alert_ids = params.get('alert_ids')
    if alert_ids:
        payload.get('params', {}).update({'alertids': get_string_to_list(alert_ids)})
    action_ids = params.get('action_ids')
    if action_ids:
        payload.get('params', {}).update({'actionids': get_string_to_list(action_ids)})
    event_ids = params.get('event_ids')
    if event_ids:
        payload.get('params', {}).update({'eventids': get_string_to_list(event_ids)})
    group_ids = params.get('group_ids')
    if group_ids:
        payload.get('params', {}).update({'groupids': get_string_to_list(group_ids)})
    host_ids = params.get('host_ids')
    if host_ids:
        payload.get('params', {}).update({'hostids': get_string_to_list(host_ids)})
    user_ids = params.get('user_ids')
    if user_ids:
        payload.get('params', {}).update({'userids': get_string_to_list(user_ids)})
    object_ids = params.get('object_ids')
    if object_ids:
        payload.get('params', {}).update({'objectids': get_string_to_list(object_ids)})
    application_ids = params.get('application_ids')
    if application_ids:
        payload.get('params', {}).update({'applicationids': get_string_to_list(application_ids)})
    event_object_type = params.get('event_object_type')
    if event_object_type:
        payload.get('params', {}).update({'eventobject': EVENT_OBJECT_TYPE_MAP.get(event_object_type)})
    event_source = params.get('event_source')
    if event_source:
        payload.get('params', {}).update({'eventsource': EVENT_SOURCE_MAP.get(event_source)})
    source = params.get('source')
    if source:
        payload.get('params', {}).update({'source': EVENT_SOURCE_MAP.get(source)})
    sort_field = params.get('sort_field')
    if sort_field:
        payload.get('params', {}).update({'sortfield': sort_field})
    sortorder = params.get('sortorder')
    if sortorder:
        payload.get('params', {}).update({'sortorder': sortorder})
    limit = params.get('limit')
    if limit:
        payload.get('params', {}).update({'limit': limit})
    acknowledged = params.get('acknowledged')
    if acknowledged:
        payload.get('params', {}).update({'acknowledged': acknowledged})
    suppressed = params.get('suppressed')
    if suppressed:
        payload.get('params', {}).update({'suppressed': suppressed})
    severities = params.get('severities')
    if severities:
        payload.get('params', {}).update({'severities': severities})
    event_id_from = params.get('event_id_from')
    if event_id_from:
        payload.get('params', {}).update({'eventid_from': event_id_from})
    event_id_till = params.get('event_id_till')

    if event_id_till:
        payload.get('params', {}).update({'eventid_till': event_id_till})

    additional_fields = params.get('additional_fields', {})
    if additional_fields:
        payload.get('params', {}).update(additional_fields)
    payload = json.dumps(payload)
    return payload


def get_alerts(config, params):
    api_client = Zabbix(config)
    rpc_json_payload = {
        "jsonrpc": "2.0", "method": "alert.get", "params": {}, "id": 1
    }
    request_payload = build_rpc_request_payload(params, rpc_json_payload)
    resp = api_client.make_api_call(payload=request_payload)
    return parse_response(resp)


def get_events(config, params):
    api_client = Zabbix(config)
    rpc_json_payload = {"jsonrpc": "2.0", "method": "event.get", "params": {}, "id": 1
                        }
    request_payload = build_rpc_request_payload(params, rpc_json_payload)
    return api_client.make_api_call(payload=request_payload)


def get_problems(config, params):
    api_client = Zabbix(config)
    rpc_json_payload = {"jsonrpc": "2.0", "method": "problem.get", "params": {}, "id": 1
                        }
    request_payload = build_rpc_request_payload(params, rpc_json_payload)
    return api_client.make_api_call(payload=request_payload)


def execute_generic_rest_api_call(config, params):
    api_client = Zabbix(config)
    payload = params.get('request_body')
    return api_client.make_api_call(payload=json.dumps(payload))


def _check_health(config):
    api_client = Zabbix(config)
    rpc_json_payload = {
        "jsonrpc": "2.0", "method": "alert.get", "params": {"limit": 1}, "id": 1
    }
    return api_client.make_api_call(payload=json.dumps(rpc_json_payload))


operations = {
    'get_alerts': get_alerts,
    'get_events': get_events,
    'get_problems': get_problems,
    'execute_generic_rest_api_call': execute_generic_rest_api_call
}
