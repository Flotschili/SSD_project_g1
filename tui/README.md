TODO


### Generate client
```bash
pip install openapi-python-client
```
```bash
openapi-python-client generate --path ..\brewery-openapi.yaml
```
```bash
poetry add ./beer-hub-client
```


### Update client
```bash
poetry remove beer-hub-client
```
```bash
openapi-python-client generate --path ..\brewery-openapi.yaml --overwrite
```
```bash
poetry add ./beer-hub-client
```
#### If generating fails you have to reinstall the openapi-python-client
```bash
pip uninstall openapi-python-client
```
```bash
pip install openapi-python-client
```

## Adapt OpenAPI Spec
The automatically generated openapi spec from django has a few inconsistencies.
### Correct return object from login


Adapt the /auth/login/ response:
```yaml
      responses:
        "200":
          description: ""
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/LoginKey'
```

Add following to components/schemas:
```yaml
    LoginKey:
      type: object
      properties:
        key:
          title: Key
          type: string
```