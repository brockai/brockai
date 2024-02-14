match_all_query = {
    "query": {
        "match_all": {}
    }
}

default_index_settings = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 1,
    }
}

tenant_index_mappings = {
    "mappings": {
        "properties": {
            "name": {"type": "keyword"},
            "given_name": {"type": "text"},
            "email": {"type": "keyword"},
            "app_redirects": {"type": "object"},
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
