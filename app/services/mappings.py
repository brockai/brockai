match_all_query = {
    "query": {
        "match_all": {}
    },
    "size": 1000
}

match_tenant_files_query = {
    "query": {
        "match_all": {}
    },
    "_source": ["file_name", "file_size"],
    "size": 100
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

logs_mappings = {
    "mappings": {
        "properties": {
            "type": {"type": "keyword"},
            "message": {"type": "text"},
            "service": {"type": "text"},
            "tenant_id": {"type": "text"},
            "create_data": {"type": "date"},
        }
    }
}


files_mappings = {
    "mappings": {
        "properties": {
            "file_name": {"type": "keyword"},
            "created_date": {"type": "date"},
            "file_size": {"type": "integer"},
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