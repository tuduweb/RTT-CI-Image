## RTT-CI-Image

Some CI related to RTT

### step

1. build the docker image

	`docker build -t ciimage:latest .`

2. simple run

	`docker run -it --mount type=bind,source=~/development/CI/mountPkg,target=/mount1 ciimage:latest`


### Reference

1. [Caching Docker builds in GitHub Actions: Which approach is the fastest?🤔A research.](https://dev.to/dtinth/caching-docker-builds-in-github-actions-which-approach-is-the-fastest-a-research-18ei)