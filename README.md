Dokcer Networking Benchmark
===========================

TODO: describe the whole thing

How to make my tests?
=====================

Render experiments compose/swarm files:

    $ make -C src/main/python/ experiments

Build `iperf` image:

    $ make -C src/main/docker/iperf

Deploy your stack (on swarm or compose):

    $ docker stack deploy --resolve-image never \
        -c src/main/python/target/your-experiment.yml
    $ docker-compose \
        -f src/main/python/target/your-experiment.yml
        up

Monitor its execution:

    $ bash src/main/bash/follow-logs.sh # to follow sink logs
    $ bash src/main/bash/follow-logs.sh source # to follow source logs

Save the data:

    $ bash src/main/bash/save-sink-logs.sh

Last, but not least, deal with the bugs and submit your PRs.

ps: inside `src/main/awk` there is a script to help you to make sense of your data.

TODO
====

 - Automate this whole mess
 - Automate it again
 - Make an actual "service" for these tasks
 - Fix `tsung` or migrate to `Siege` or `Gatling`

