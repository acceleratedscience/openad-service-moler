# Moler Inference Service

<!-- description -->
<!-- /description -->

Generation Service for Sky Server

1. Install Sky  with `pip install "skypilot-nightly[aws]"`

2. setup your aws command line

3. run `sky check`

4. run `sky serve up generation_service.yaml`
This will take about 10 minutes to deploy  it can be monitored through the controllers logs.
e.g. `sky serve logs sky-service-0af4  --controller`
