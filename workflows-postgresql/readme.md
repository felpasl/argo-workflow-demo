# setup

```
# deploy a simple postgresql
kubectl apply -f postgres.yaml
 
# Register a Workflow Template to initialize the database
kubectl apply -f templates.yaml

# Submit a workflow instance with parameters
argo submit --watch --from wftmpl/fill-postgres --parameter message=teste
```

## Explanation of templates.yaml

```yaml
  - name: run-postgres
    inputs:
      parameters:
      - name: sql     
    container: 
      image: postgres:alpine
      envFrom:
      - secretRef:
          name: postgres-secret
      command: [ sh, -c ]
      args: ['PGPASSWORD=$(POSTGRES_PASSWORD) psql -U $(POSTGRES_USER) -h $(POSTGRES_HOST) -d $(POSTGRES_DB) -p $(POSTGRES_PORT) -c "{{inputs.parameters.sql}}"']
    
```
The configuration above defines a PostgreSQL container named run-postgres within the workflow. Please be aware that the usage of `{{inputs.parameters.sql}}` as a command input within this context can lead to SQL injection vulnerabilities if applied outside of educational scenarios.

```yaml
    - - name: fill-table
        template: run-postgres
        arguments:
          parameters:
          - name: sql
            value: "CREATE TABLE IF NOT EXISTS messages (message VARCHAR(255)); INSERT INTO messages (message) VALUES ('{{inputs.parameters.message}}');"
```
The value of `message` passed as a parameter is used to insert data into a table. 

However, it's important to understand that directly injecting user input into SQL queries, as demonstrated here, is unsafe and should never be done in production systems.

Utilize Python in conjunction with a PostgreSQL framework, or alternatively, select an appropriate programming language, to proactively safeguard against SQL injection vulnerabilities.

## Disclaimer: SQL Injection Ignored for Educational Purposes

The following workflow or demonstration intentionally ignores considerations and safeguards against SQL injection for the sole purpose of providing an educational example. SQL injection is a serious security vulnerability that can lead to unauthorized access, data breaches, and other malicious activities in real-world applications.


# Basic Events

https://argoproj.github.io/argo-workflows/events/

https://argoproj.github.io/argo-workflows/access-token/

```yaml
apiVersion: argoproj.io/v1alpha1
kind: WorkflowEventBinding
metadata:
  name: event-consumer
spec:
  event:
    # metadata header name must be lowercase to match in selector
    selector: payload.message != "" && discriminator == "my-event"
  submit:
    workflowTemplateRef:
      name: fill-postgres
    arguments:
      parameters:
      - name: message
        valueFrom:
          event: payload.message
```
- This YAML configuration defines an event binding named event-consumer.
- It specifies a condition in the `selector` field that filters incoming events based on the presence of a non-empty message in the payload and the event discriminator being "my-event".
- When the conditions are met, the workflow template `fill-postgres` will be triggered.
- The event payload's message will be used as an argument named `message` for the triggered workflow.

```bash
# Apply the EventBinding YAML
kubectl apply -f event.yaml

# Create a role with necessary permissions
kubectl apply -f roles.yaml

# Create a Kubernetes secret for the service account token
kubectl apply -f - <<EOF
apiVersion: v1
kind: Secret
metadata:
  name: app-sa.service-account-token
  annotations:
    kubernetes.io/service-account.name: app-sa
type: kubernetes.io/service-account-token
EOF

# Retrieve and decode the service account token
ARGO_TOKEN="Bearer $(kubectl get secret app-sa.service-account-token -o=jsonpath='{.data.token}' | base64 --decode)"

# Send an event to argo using cURL
curl http://localhost:2746/api/v1/events/default/my-event -H "Authorization: $ARGO_TOKEN" -d '{"message": "hello events"}'

```

# Event-Source

## Argo Events

Argo Events is an event-driven workflow automation framework for Kubernetes. It allows you to trigger K8s objects, Argo Workflows, Serverless workloads, and more based on events from various sources such as webhooks, S3, schedules, messaging queues, GCP Pub/Sub, SNS, SQS, and others.

In this sample, an API call is used to trigger a workflow template.

For more information on how to use Argo Events, please refer to the documentation.

https://argoproj.github.io/argo-events/


## Install

To install Argo Events, please refer to the [installation documentation](https://argoproj.github.io/argo-events/installation/).

**Important:** An event bus must be deployed in the same namespace as the event source and sensor.

## Event Source YAML File
This YAML file defines an event source and a sensor that listens for events from the source and triggers an Argo Workflow when an event is received.

### Event Source
The event source is defined in the first part of the YAML file. It is named "webhook" and listens for an event named "example" on port 12000 using the HTTP POST method. When an event is received, it triggers a Sensor resource named "webhook" in the second part of the YAML file.

### Sensor
The Sensor resource is defined in the second part of the YAML file. It is named "webhook" and has a template that specifies a service account named "app-sa". The Sensor has a dependency on an event source named "webhook" and an event named "example". When the event is received, it triggers a trigger named "argo-workflow-trigger".

#### Trigger
The trigger is defined in the "triggers" section of the Sensor resource. It is named "argo-workflow-trigger" and specifies an Argo Workflow operation of "submit". The trigger passes a parameter named "message" to the Argo Workflow with the value of the "body.message" field from the received event.


