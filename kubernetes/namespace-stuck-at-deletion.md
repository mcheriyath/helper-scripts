#### Run the following command to view the namespaces that are stuck in the Terminating state
```
kubectl get namespaces
```

#### Select a terminating namespace and view the contents of the namespace to find out the finalizer. Run the following command:
```
kubectl get namespace <namespace> -o yaml
```

#### Identify the reason for the supposedly stuck state.
```
kubectl api-resources --verbs=list --namespaced -o name \
  | xargs -n 1 kubectl get --show-kind --ignore-not-found -n <namespace>
```

#### Starting kubectl proxy in one terminal
```
kubectl proxy
```

#### Empty the finalizer part and upload it to the cluster.
```
kubectl get ns delete-me -o json | \
  jq '.spec.finalizers=[]' | \
  curl -X PUT http://localhost:8001/api/v1/namespaces/<namespace>/finalize -H "Content-Type: application/json" --data @-
```

#### Additionally check to see if this is caused by a kubernetes api service
```
kubectl get apiservice
```


#### If found any error(False (MissingEndpoints)) in any one of the apiservice, delete it like:
```
kubectl delete apiservice v1beta1.external.metrics.k8s.io
```

#### Persistent Volume Finalizers
```
kubectl patch pvc db-pv-claim -p '{"metadata":{"finalizers":null}}'
kubectl patch pod db-74755f6698-8td72 -p '{"metadata":{"finalizers":null}}'
```
