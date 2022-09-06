import yaml

config_file = "C:/Users/HP/PycharmProjects/pythonRequestsApiFramework/config/config.yml"

with open(config_file, 'r')as stream:
    cfg = yaml.safe_load(stream)
    BASE_URL = cfg['base_url']
    API_PATH = cfg['api_path']
    USERNAME = cfg['username']
    PASSWORD = cfg['password']
    USER_ID = cfg['user_id']
