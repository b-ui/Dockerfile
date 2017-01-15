import functools
import json
import os


def singleton(class_):
    instances = {}

    def get_instance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return get_instance


conf_mapping = {
    'TESTING': 'feature_testing.json',
    'PRODUCTION': 'feature_production.json'
}


def get_feature_config_file():
    _mode = os.environ.get('MODE')
    _feature_config_file = os.environ.get('FEATURE_CONFIG_FILE')

    if _mode == 'PRODUCTION' and _feature_config_file:
        return _feature_config_file

    feature_file = conf_mapping.get(_mode)
    if feature_file is None:
        feature_file = 'feature_default.json'

    base_path = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(base_path, feature_file)


@singleton
class Features(object):
    class Feature(object):
        def __init__(self, f_name, active):
            self.name = f_name
            self._active = active

        @property
        def active(self):
            # if not self._active:
            #     logging.warning('Feature {} is not active'.format(self.name))
            return self._active

    def __init__(self, conf_file):
        with open(conf_file) as f:
            self.features_config = json.load(f)
        self.features = {}

    def __call__(self, f_name):
        try:
            return self.features[f_name]
        except KeyError:
            active = self.features_config.get(f_name, False) \
                     and self.features_config.get(f_name).get('active', False)
            self.features[f_name] = self.Feature(f_name, active)
            return self.features[f_name]


features = Features(get_feature_config_file())


def feature_with(f_name):
    def feature_wrapper(func):
        @functools.wraps(func)
        def feature(*args, **kwargs):
            func_return = None
            if features(f_name).active:
                func_return = func(*args, **kwargs)
            return func_return

        return feature

    return feature_wrapper
