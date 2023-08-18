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