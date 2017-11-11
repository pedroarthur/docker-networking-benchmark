from yaml import dump
from collections import namedtuple

Experiment = namedtuple('Experiment', ['algorithm', 'n_nodes', 'size', 'swarm_nodes'])

class ExperimentBuilder(object):

    def __init__(self, composer):
        self.composer = composer

    def build(self, experiment):
        name = '%s-%d-%d.yml' % (
            experiment.algorithm.__name__,
            experiment.n_nodes,
            experiment.size,
        )

        env = {
            'EXPERIMENT_SIZE': experiment.n_nodes,
        }

        topology = experiment.algorithm(experiment.n_nodes, experiment.size)

        placement = [0] * experiment.n_nodes

        sources = {s for s,_ in topology}
        sinks = {t for _,t in topology}

        for l in [sources, sinks]:
            for i, s in enumerate(l):
                placement[s] = i % experiment.swarm_nodes

        composed = self.composer.to_dict(topology, placement, env)

        return name, dump(composed, default_flow_style=False)

if __name__ == '__main__':
    from topology import mesh, direct_connection, star, tree
    from composer import Composer, IperfBaseImage, NoLocalityRender
    from composer import SwarmStructureRender, SwarmLocalityRender

    swarm_builder = ExperimentBuilder(Composer(
        SwarmStructureRender(),
        IperfBaseImage(),
        SwarmLocalityRender()))

    experiments = [
        (    'local', swarm_builder, Experiment(direct_connection, 96, -1, 1)),
        (    'local', swarm_builder, Experiment(             mesh, 96, 12, 1)),
        (    'local', swarm_builder, Experiment(             star, 96, 24, 1)),
        (    'local', swarm_builder, Experiment(             tree, 96,  4, 1)),
        ('placement', swarm_builder, Experiment(direct_connection, 96, -1, 2)),
        ('placement', swarm_builder, Experiment(             mesh, 96, 12, 2)),
        ('placement', swarm_builder, Experiment(             star, 96, 24, 2)),
        ('placement', swarm_builder, Experiment(             tree, 96,  4, 2)),
    ]

    for prefix, builder, experiment in experiments:
        name, data = builder.build(experiment)
        path_name = 'target/%s-%s' % (prefix, name)

        with open(path_name, 'w') as f:
            print("writing", path_name)
            f.write(data)

