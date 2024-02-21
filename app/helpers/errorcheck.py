import requests

def check_opensearch_health():
    url = 'http://localhost:9200/_cluster/health'

    try:
        response = requests.get(url)
        if response.status_code == 200:
            health_info = response.json()
            print(f"Cluster status: {health_info['status']}")
        else:
            print(f"Failed to fetch cluster health. Status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"Error: {e}")

# Call the function to check the OpenSearch cluster health
# check_opensearch_health()
