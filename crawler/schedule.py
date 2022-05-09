import yaml

with open('schedule.json', 'r') as f:
    spiders = yaml.load(f, Loader=yaml.FullLoader)
    for k, v in spiders.items():
        print(k, v)
