pykubectl
=========

Synopsis
--------

These are Python scripts and snippets for doing kubectl type stuff directly against the Kubernetes API endpoints

This is a **work in progress**. Don't expect anything in here to stay stable.

Once things *do* become stable, documentation will be updated to reflect reality.

Example
-------

For now, all `make` does is assume newly-created `role/TheAvengers` and attempt to connect to each of our EKS clusters with it (you need to have your AWS credentials configured for this. See Michael's Confluence link below for hints.)

The list of EKS clusters is generated dynamically via a Boto3 call. The script then queries `aws-auth` for the presence of `role/TheAvengers` just as an example of how to access ConfigMaps. 

This script is in a heavy state of development, and there is no warranty as to fitness for a particular purpose nor any optimization whatsoever implied. This code may run poorly, or not at all. If you want to steal portions of code, go ahead, but I make no claim that any of this is the right way to do things yet. (That will come later).

```
~/pykubectl (master)
[1]michael@smo-mtalarczyk$ make
Installing dependencies from Pipfile.lock (3d7b14)…
  🐍   ▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉ 23/23 — 00:00:02
To activate this project's virtualenv, run pipenv shell.
Alternatively, run a command inside the virtualenv with pipenv run.
All dependencies are now up-to-date!
aero                 ✓
goat                 ✓
noleeches            ✓
sparkle              ✓
strawman             ✗
swat                 ✓
vision               ✓
batman               ✗
dsp-prod             ✗ (no config found)
cicd-test            ✗
stray                ✓
tornado              ✓
venom                ✓
dsp-bidder-prod      ✗ (no config found)
cicd                 ✗
galactus             ✓
orphan               ✓
pacman               ✗
```

See Also
--------
* [Michael's Role-based EKS Access Proposal](https://videoamp.atlassian.net/wiki/spaces/~789927745/pages/1043136602/Michael+s+Role-based+EKS+Access+Proposal)
