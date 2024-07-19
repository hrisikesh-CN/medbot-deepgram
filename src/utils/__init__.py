import yaml


def load_config(config_path)-> dict:
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    db_config = config.get('database', {})

    return db_config

def get_appointment_database_url():
    config_path = '../config/database_config.yml'
    db_config = load_config(config_path)
    return db_config.get('appointments', {}).get('url')
