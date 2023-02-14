# oi-bus

> I mean, like, a serial or parallel bus, not bus as a vehicle.

oi-bus is a Django application designed to help run on-site sports programming
competitions, most specifically
[Polish Olympiad in Informatics](https://oi.edu.pl) and
[Algorithmic Engagements](https://potyczki.mimuw.edu.pl).

It can be used to:

- manage participants' workstations (including more complex operations using
  Ansible),
- manage dnsmasq configuration to set the workstations' IP addresses in stone,
- manage assignment of participants to workstations,
- provide the aforementioned assignment to
  [oioioi](https://github.com/sio2project/oioioi)'s ipauthsync module, so that
  the participants are automagically logged in to SIO2 based on the
  workstations' IP addresses,
- allow participants to back their files up to make things easier when their
  workstation suddenly bursts into flames, or less poetically, suffers an
  unrecoverable hard drive failure,
- allow participants to print text files during the competition.

## Requirements and building

You ought to be running Debian 11 on amd64 architecture. It could run on
something else, but it might not, and we have not tested it on anything other
than what we just said.

You need to install `build-essential` package, which contains Debian's
packaging tools.

`make build` - builds .deb packages. Output will be placed in ./out directory.
`make clean` - removes ./out directory.

`dpkg-buildpackage` might tell you you're missing some packages. Install those
and run it again.

## Building in docker

Alternatively you may build packages using docker.

`make` - builds .deb packages. Output will be placed in ./out directory.

`make clean-docker` - removes ./out directory.
