from collections import OrderedDict

from dnslib import RR


class RulesManager(object):
    _rules_tables = OrderedDict()
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    @classmethod
    def load_rules(cls, rules):
        for rule in rules:
            zone = None
            try:
                zone = RR.fromZone(rule)
            except Exception:
                print('[e] Malformed rule -- {rule}'.format(rule=rule))
                continue
            domain = rule.split()[0]
            cls._rules_tables[domain] = zone

    @classmethod
    def match(cls, label):
        rules = cls._rules_tables.keys()

        for rule in rules:
            if label.matchGlob(rule):
                return cls._rules_tables[rule]
        return None
