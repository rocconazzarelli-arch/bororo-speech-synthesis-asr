# Data directory

The original course folder contained a Bororo–Portuguese dictionary, but no explicit redistribution license was bundled with it. The dictionary is therefore not included in this public repository.

To run the notebooks, place an authorized JSON export here as:

```text
data/boe-dict-20240805.json
```

Expected minimal structure:

```json
{
  "bororo_term": "Portuguese gloss"
}
```

The generator also accepts richer records such as:

```json
{
  "bororo_term": {
    "desc": "Portuguese gloss",
    "token_list": [],
    "sent_list": []
  }
}
```
