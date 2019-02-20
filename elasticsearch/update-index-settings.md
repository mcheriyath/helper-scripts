#### Issue: `Limit of total fields [1000] in index [index_name] has been exceeded`

_Temporary Solution:_

```
(~)-()--> curl -XPUT 'https://search-domain_name.us-east-1.es.amazonaws.com/index_name/_settings' -H 'Content-Type: application/json' -d'
{
  "index" : {
    "mapping" : {
      "total_fields" : {
        "limit" : "10000"
      }
    }
  }
}'
{"acknowledged":true}
```
_Confirm_

```
(~)-()--> curl -XGET 'https://search-domain_name.us-east-1.es.amazonaws.com/index_name/_settings?pretty'
{
  "jenkins-data-2019.02.20" : {
    "settings" : {
      "index" : {
        "mapping" : {
          "total_fields" : {
            "limit" : "10000"
          }
        },
        "number_of_shards" : "5",
        "provided_name" : "index_name",
        "creation_date" : "1550624929122",
        "number_of_replicas" : "1",
        "uuid" : "Acosqxk6QR6_YfsdasdasdasdsadasdasdTKEA",
        "version" : {
          "created" : "6040299"
        }
      }
    }
  }
}
```
#### _Perm Fix_ <br>
Get the current template name:
```
curl -X GET 'https://search-index_name.us-east-1.es.amazonaws.com/_template'
```
Update the limit in the template
```
curl -XPUT https://search-index_name.us-east-1.es.amazonaws.com/_template/kibana_index_template -H 'Content-Type: application/json' -d \
'{
	"template": "*",
	"order": 0,
	"settings": {
		"index": {
			"mapping": {
				"total_fields": {
					"limit": "10000"
				}
			}
		}
	},
	"version": 1
}'
{"acknowledged":true}
```
_Confirm_
```
curl -X GET 'https://search-index_name.us-east-1.es.amazonaws.com/_template'
```
