from collections import defaultdict

base_compose = {
    'version': '2.0',
    'services': {
        #'master': {
        #    'image': "master"
        #}
    },
}

class ComposeStructureRender(object):

    def base(self):
        raise NotImplementedError

    def service(self):
        raise NotImplementedError


class SwarmStructureRender(ComposeStructureRender):

    def __init__(self, version='3.0'):
        self.version = version

    def base(self):
        return {
            'version': self.version,
            'services': {},
            'networks': {
                'wanderley': {
                    'driver': 'overlay'
                }
            }
        }

    def service(self):
        return {
            'networks': [ 'wanderley' ]
        }


def make_node_name(node):
    return '{}'.format(node)


def make_host_name(host, source=False):
    return 'host-{}'.format(host)


class LocalityRender(object):

    def locality(self, locality):
        raise NotImplementedError


class NoLocalityRender(LocalityRender):

    def locality(self, _):
        return {}


class SwarmLocalityRender(LocalityRender):

    def locality(self, locality):
        return {
            'deploy': {
                'mode': 'replicated',
                'replicas': 1,
                'placement': {
                    'constraints': [
                        'node.labels.experiment.node == %s' % (locality),
                    ],
                },
            },
        }


class BaseImage(object):
    def source(self, source, targets):
        raise NotImplementedError

    def target(self, target):
        raise NotImplementedError


class TsungBaseImage(BaseImage):

    def __init__(self):
        self.source_image = 'tsung-client'
        self.target_image = 'tsung-server'

    def source(self, source, targets):
        return {
            'image': self.source_image,
            'environment': {
                'TARGETS': ' '.join(targets),
            },
            'depends_on': targets,
        }

    def target(self, target):
        return {
            'image': self.target_image,
        }


class IperfBaseImage(BaseImage):

    def source(self, source, targets, environment={}):
        return {
            'image': 'iperf:debian-testing',
            'entrypoint': 'parallel-iperf' ,
            'command': [t for t in targets],
            'depends_on': [t for t in targets],
            'environment': {
                **{'IPERF_TIME': 60},
                **environment,
            },
            'labels': [
                'experiment.source=true'
            ],
        }

    def target(self, target):
        return {
            'image': 'iperf:debian-testing',
            'labels': [
                'experiment.sink=true'
            ],
        }


class Composer(object):

    def __init__(self, compose_structure, base_image, locality_render):
        self.compose_structure = compose_structure
        self.base_image = base_image
        self.locality_render = locality_render

    def to_dict(self, source_target, locality, source_env={}):
        groups = defaultdict(list)
        result = { **self.compose_structure.base() }

        for s,t in source_target:
            groups[s].append(t)

        for s, t in groups.items():
            targets = [ (i, make_host_name(i)) for i in t ]

            nodes = {
                t: self.make_target(t, make_node_name(locality[i]))
                for i,t in targets
                if t not in result['services']
            }

            source = make_host_name(s, source=True)
            if source not in result['services']:
                targets = [make_host_name(i) for i in t]
                nodes[source] = self.make_source(
                    source, targets, make_node_name(locality[s]), source_env)

            result['services'] = {
                **result['services'],
                **nodes,
            }

        return result

    def make_target(self, target, locality):
        return {
            **self.compose_structure.service(),
            **self.base_image.target(target),
            **self.locality_render.locality(locality),
        }

    def make_source(self, source, targets, locality, source_env):
        return {
            **self.compose_structure.service(),
            **self.base_image.source(source, targets, source_env),
            **self.locality_render.locality(locality),
        }


if __name__ == '__main__':
    from pprint import pprint

    test = [
            (0, 1), (0, 3), (0, 5),
            (2, 1), (2, 3), (2, 5),
            (4, 3), (4, 5), (4, 7),
            (6, 5), (6, 7), (6, 9),
            (8, 7), (8, 9), (8, 11),
            (10, 9), (10, 11), (10, 13),
            (12, 11), (12, 13), (12, 15),
            (14, 11), (14, 13), (14, 15)]

    locality = [i%2 for i in range(16)]

    composer = Composer(
            SwarmStructureRender(),
            IperfBaseImage(),
            SwarmLocalityRender())
    pprint(composer.to_dict(test, locality))

