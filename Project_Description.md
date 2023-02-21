# MLOps Final Project Planning

1. Problem description
	- [x] Problem is well described and it's clear what the problem the project solves

2. Cloud
	- [ ] Minimum:	The project is developed on the cloud OR the project is deployed to Kubernetes or similar container management platforms
	- [x] Best: 	The project is developed on the cloud and IaC tools are used for provisioning the infrastructure

3. Experiment tracking and model registry
	- [x] Both experiment tracking and model registry are used

4. Workflow orchestration
	- [ ] Minimum:	Basic workflow orchestration
	- [ ] Best: 	Fully deployed workflow

5. Model deployment
	- [ ] Minimum:	Model is deployed but only locally
	- [x] Best: 	The model deployment code is containerized and could be deployed to cloud or special tools for model deployment are used

6. Model monitoring
	- [ ] Minimum:	Basic model monitoring that calculates and reports metrics
	- [ ] Best: 	Comprehensive model monitoring that send alerts or runs a conditional workflow (e.g. retraining, generating debugging dashboard, switching to a different model) if the defined metrics threshold is violated

7. Reproducibility
	- [x] Minimum:	Some instructions are there, but they are not complete
	- [ ] Best: 	Instructions are clear, it's easy to run the code, and the code works. The version for all the dependencies are specified.

### Best practices
- [x] There are unit tests (1 point)
- [ ] There is an integration test (1 point)
- [x] Linter and/or code formatter are used (1 point)
- [x] There's a Makefile (1 point)
- [x] There are pre-commit hooks (1 point)
- [ ] There's a CI/CD pipeline (2 points)
