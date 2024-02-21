match_all_query = {
    "query": {
        "match_all": {}
    },
    "size": 1000
}

file_query = {
    "query": {
        "ids": {
        "values": ['NPddwo0Bs3h86QjiE4I5']
        }
    },
    "size": 10000,
    "timeout": "300s"
}

admin_role = {"roles":[{"name":'tenant'},{"name":'admin'}]}
tenant_role = {"roles":[{"name":'tenant'}]}

pipelines = {"pipelines":[{"name":'platform-nlp-ingest'}]}
models = {"models":[{"name":'msmarco-distilbert-base-tas-b'}]}

default_index_settings = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 1,
    }
}

#types: error, acknowledged, test
platform_log_mappings = {
    "mappings": {
        "properties": {
            "type": {"type": "keyword"},
            "tenant_id": {"type": "keyword"},
            "message": {"type": "text"},
            "service": {"type": "text"},
            "timestamp": {"type": "date"}
        }
    }
}

platform_index_mappings = {
    "mappings": {
        "properties": {
            "name": {"type": "keyword"},
            "roles": {"type": "object"},
            "models":  {"type": "object"},
            "pipelines":  {"type": "object"},
            "tenants": {"type": "object"}
        }
    }
}

tenant_index_mappings = {
    "mappings": {
        "properties": {
            "name": {"type": "keyword"},
            "given_name": {"type": "text"},
            "email": {"type": "keyword"},
            "role":  {"type": "object"},
        }
    }
}

files_index_mappings = {
    "mappings": {
        "properties": {
            "file_name": {"type": "keyword"},
            "created_date": {"type": "date"},
            "file_size": {"type": "integer"},
            "data_extraction": {"type": "text"},
            "classification": {"type": "text"},
            "compliancy_check": {"type": "text"},
            "risk_assessment": {"type": "text"},
            "file": {
                "properties": {
                    "content": {
                        "type": "binary"
                    }
                }
            }
        }
    }
}