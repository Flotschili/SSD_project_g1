# BeerHub Tui
## TL;DR Start Application
### Generate client
```bash
openapi-python-client generate --path ..\brewery-openapi.yaml --overwrite
```
```bash
poetry add ./beer-hub-client
```
### Start TUI
Run `__main__` file.


## After fetching new version of the OpenAPI Spec
### Adapt OpenAPI Spec
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

### Rename /beers/name/{beer_name}/
Search for `/beers/name/{beer_name}/`.
Adapt `operationId: beers_get_beer_by_name_2`.