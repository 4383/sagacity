# Sagacity

Visualize hidden patterns in your project history.

Sagacity allow you to audit our projects to observe hidden patterns.

It allow you to generate graph to monitor authors behaviors. It could
by used to improve your project UX or to improve how you manage our projects.

Sagacity explore project's git history to generate graph and allow you to
observe patterns.


## Usages

Simple usage, monitor the current working dir git history:

```sh
tox -e venv -- sagacity
```

Monitor a specific working dir history:

```sh
tox -e venv -- sagacity </your/path>
```

Monitor a specific period:

```sh
tox -e venv -- sagacity --since 2020-09-01 --until 2020-09-20 </your/path>
```

Monitor the activity of a specific stagged directory during a specific period:

```sh
tox -e venv -- sagacity \
    --since 2020-09-01 \
    --until 2020-09-20 \
    --path <stagged/path>
    </your/path>
```

Concrete example, monitor the activity of
[openstack/releases](https://opendev.org/openstack/releases) and especially
of the [Wallaby serie](https://releases.openstack.org/wallaby/schedule.html#w-rc1)
since a specific date (the begining date).

```
$ git clone https://opendev.org/openstack/releases
$ cd releases
$ tox -e venv -- sagacity \
    --since "2020-10-12" \
    --path deliverables/wallaby \
    --branch origin/master
```

The previous example could help us to highlight some hidden pareto laws and patterns
during this observed period, by example it could help to identify which team release
their deliverables more often than others to allow us to help them proactively.
By example by observing who are the team who deliver many releases candidates
just before the deadline, maybe it could be due to project characteristics, or
also to team's organization.
