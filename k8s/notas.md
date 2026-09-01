# minikube y kubectl

> Prerrequisito: tener instalado Docker y k8s. Para instalar k8s seguie esta [guia](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/)

## Instalando y corriendo minikube por primera vez

Instalar minikube siguiendo esta [guia](https://minikube.sigs.k8s.io/docs/start/), y a kubectl con esta otra [guia](https://kubernetes.io/es/docs/tasks/tools/install-kubectl/)

una vez instalado podemos inicializar a minikube de la siguiente manera:

```bash
minikube start
```

Aunque la version de `kubernetes` que use el cluster, puede diferir de la que tenemos en nuestra maquina con `kubectl`. Para arreglar esto, primero hay que ver que version de k8s se usa el comando -> `kubectl version --client`

```bash
kubectl version --client
Client Version: version.Info{Major:"1", Minor:"22", GitVersion:"v1.22.3", GitCommit:"c92036820499fedefec0f847e2054d824aea6cd1", GitTreeState:"clean", BuildDate:"2021-10-27T18:41:28Z", GoVersion:"go1.16.9", Compiler:"gc", Platform:"linux/amd64"}
```

la version es `v1.22.3`, con lo cual podemos inicializar a minikube de esta manera:

```bash
$ minikube start --kubernetes-version=v1.22.3
😄  minikube v1.24.0 on Debian 11.1
✨  Using the docker driver based on existing profile
👍  Starting control plane node minikube in cluster minikube
🚜  Pulling base image ...
💾  Downloading Kubernetes v1.22.3 preload ...
    > preloaded-images-k8s-v13-v1...: 501.73 MiB / 501.73 MiB  100.00% 22.50 Mi
🔄  Restarting existing docker container for "minikube" ...
🐳  Preparing Kubernetes v1.22.3 on Docker 20.10.7 ...
🔎  Verifying Kubernetes components...
    ▪ Using image kubernetesui/dashboard:v2.3.1
    ▪ Using image kubernetesui/metrics-scraper:v1.0.7
    ▪ Using image gcr.io/k8s-minikube/storage-provisioner:v5
🌟  Enabled addons: storage-provisioner, default-storageclass, dashboard
🏄  Done! kubectl is now configured to use "minikube" cluster and "default" namespace by default
```

De esta manera tenemos inicializado a minikube y listo para desplegar un cluster.

### Dashboard y metrics server

Podemos inicializar el dashboard de esta manera 

```bash
minikube dashboard
```

Esto deberia abrir en el navegador el dashboard de nuestro cluster, sino otra manera mas simple es que nos de un link local para acceder al dashboard de esta manera:

```bash
$ minikube dashboard --url
🤔  Verifying dashboard health ...
🚀  Launching proxy ...
🤔  Verifying proxy health ...
http://127.0.0.1:34371/api/v1/namespaces/kubernetes-dashboard/services/http:kubernetes-dashboard:/proxy/
```

Puede verse mas de esto [aqui](https://minikube.sigs.k8s.io/docs/handbook/dashboard/)

Sobre la dependencia de `metrics-server` ([repo](https://github.com/kubernetes-sigs/metrics-server)), esta es en realidad una [extension (Addon)](https://kubernetes.io/docs/concepts/cluster-administration/addons/), y hay que instalarlo a mano, dependiendo en donde este nuestro cluster.

En el caso de minikube podemos ver los addons disponibles de esta manera:

```bash
minikube addons list
```

Esto nos va a dar la lista similar a la siguiente:


|         ADDON NAME          | PROFILE  |    STATUS    |      MAINTAINER       |
|-----------------------------|----------|--------------|-----------------------|
| ambassador                  | minikube | disabled     | unknown (third-party) |
| auto-pause                  | minikube | disabled     | google                |
| csi-hostpath-driver         | minikube | disabled     | kubernetes            |
| dashboard                   | minikube | enabled ✅   | kubernetes            |
| default-storageclass        | minikube | enabled ✅   | kubernetes            |
| efk                         | minikube | disabled     | unknown (third-party) |
| freshpod                    | minikube | disabled     | google                |
| gcp-auth                    | minikube | disabled     | google                |
| gvisor                      | minikube | disabled     | google                |
| helm-tiller                 | minikube | disabled     | unknown (third-party) |
| ingress                     | minikube | disabled     | unknown (third-party) |
| ingress-dns                 | minikube | disabled     | unknown (third-party) |
| istio                       | minikube | disabled     | unknown (third-party) |
| istio-provisioner           | minikube | disabled     | unknown (third-party) |
| kubevirt                    | minikube | disabled     | unknown (third-party) |
| logviewer                   | minikube | disabled     | google                |
| metallb                     | minikube | disabled     | unknown (third-party) |
| metrics-server              | minikube | disabled     | kubernetes            |
| nvidia-driver-installer     | minikube | disabled     | google                |
| nvidia-gpu-device-plugin    | minikube | disabled     | unknown (third-party) |
| olm                         | minikube | disabled     | unknown (third-party) |
| pod-security-policy         | minikube | disabled     | unknown (third-party) |
| portainer                   | minikube | disabled     | portainer.io          |
| registry                    | minikube | disabled     | google                |
| registry-aliases            | minikube | disabled     | unknown (third-party) |
| registry-creds              | minikube | disabled     | unknown (third-party) |
| storage-provisioner         | minikube | enabled ✅   | kubernetes            |
| storage-provisioner-gluster | minikube | disabled     | unknown (third-party) |
| volumesnapshots             | minikube | disabled     | kubernetes            |

basta con habilitarlo para tenerlo disponible:

```bash
minikube addons enable metrics-server
```

el resultado deberia ser:

```
$ minikube addons enable metrics-server
    ▪ Using image k8s.gcr.io/metrics-server/metrics-server:v0.4.2
🌟  The 'metrics-server' addon is enabled
```

#### Otros clusters

> Nota: esto es por si quieren instalar metrics-server en otro lugar o cluster

Dependiendo del servicio que usen para deployear el cluster, van a poder instalarlo con mayot facilidad o no. Puede seguirse la seccion de instalacion del [repo](https://github.com/kubernetes-sigs/metrics-server#installation), o bien instalarlo aplicando los componentes:

```
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```

o sino mediante [helm](https://helm.sh/), donde van a poder encontrar el [chart de metrics-server](https://artifacthub.io/packages/helm/metrics-server/metrics-server)

> Para algunos sitios como DO, hay una [dependencia](https://marketplace.digitalocean.com/apps/kubernetes-metrics-server) de un boton que son una alternativa simple y que funcionan bien con k8s 1.20 

## Secretos...

En caso de necesitar secretos, o tener que tener en algun lugar definido datos sensibles, podemos hacer uso de los `Secrets`

```yml
apiVersion: v1
data:
  password: cGFzc3dvcmQxMjM= //password123
  username: YWRtaW4= //admin
kind: Secret
metadata:
  creationTimestamp: null
  name: mongo-creds

```

Los secretos se tienen que codificar en base64, por lo que hay que siempre pasarlos de esta manera, una forma de codificar cualquier string a base64 facilmente es con el siguiente comando:

```bash
$ echo -n "iascsecret" | base64 
aWFzY3NlY3JldA==
```

Para mas informacion de los secretos podemos verlos [aqui](https://kubernetes.io/es/docs/concepts/configuration/secret/)


## Volumenes...

#### Introduccion

Mongo necesitara de volumenes que usara para escribir/leer los datos necesarios para funcionar correctamente. Por lo que tendremos que crear al menos un volumen, mas de volumenes [aqui](https://kubernetes.io/es/docs/concepts/storage/volumes/). En especial necesitaremos los [volumenes persistentes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/), 

Los [volumenes persistentes que necesitamos en minikube](https://minikube.sigs.k8s.io/docs/handbook/persistent_volumes/), son una pieza de almacenamiento en el cluster que vamos a poder proveer de manera estatica o dinamica usando algo conocido como `Storage Class` ([mas info](https://kubernetes.io/docs/concepts/storage/storage-classes/)). Ademas de los `Persisten Volumes (PV)` existen los `Persistent Volume Claims (PVC)`, que son objetos que actuan como requests para almacenamiento. Kubernetes busca por un PV de donde se pueda tomar y asignar ese almacenamiento solicitado por un PVC. Solo funciona si se tiene aprovisionamiento de volumenes dinamicos en el cluster de k8s. 

#### Entonces... como creo volumenes en minikube???

Podemos definir [volumenes locales](https://kubernetes.io/docs/concepts/storage/volumes/#local), y definir tanto volumenes persistentes como claims que pueden llegar a tomar espacion de estos volumenes.

Generalmente en minikube estan mapeados a un directorio de estos:

- /data
- /var/lib/minikube
- /var/lib/docker
- /var/lib/containerd
- /var/lib/buildkit
- /var/lib/containers
- /tmp/hostpath_pv
- /tmp/hostpath-provisioner

un ejemplo simple puede ser:

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv0001
spec:
  accessModes:
    - ReadWriteOnce
  capacity:
    storage: 256Mi
  hostPath:
    path: /data/pv0001/
```

#### En caso de crear volumenes, como seteo bien el tamianio??

Se pueden definir mediante limites, estos limites pueden ser para volumenes o para procesamiento, se puede ver mas de esto [aqui](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/)

#### Sobre directorios locales...

Podemos 

https://kubernetes.io/es/docs/concepts/storage/volumes/#ejemplo-de-configuraci%C3%B3n-hostpath

```yaml
 volumeMounts:
    - name: config
      mountPath: <PATH IN CONTAINER>
  volumes:
    - name: config
      hostPath:
        path: <YOUR LOCAL DIR PATH>
        type: Directory
```        

## Configuracion (Variables de entorno)

#### Sobre variables de entornos

Las [variables de entorno](https://kubernetes.io/docs/tasks/inject-data-application/define-environment-variable-container/) se pueden definir tranquilamente en los specs de cualquier componente que defina bien un pod o eventualmente trabaje con ellos (StatefulSets, Deployments, etc):

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: envar-demo
  labels:
    purpose: demonstrate-envars
spec:
  containers:
  - name: envar-demo-container
    image: gcr.io/google-samples/node-hello:1.0
    env:
    - name: DEMO_GREETING
      value: "Hello from the environment"
    - name: DEMO_FAREWELL
      value: "Such a sweet sorrow"
```

Aqui se puede ver que en la seccion `env` se definen los nombres de las variables de entorno, estas pueden despues tomarse o bien se secretos de de `ConfigMaps`, entre otras fuentes.

#### Sobre ConfigMaps

Una manera simple de definir configuraciones es mediante [ConfigMaps](https://kubernetes.io/es/docs/concepts/configuration/configmap/#configmaps-y-pods), y que se usan para definir valores dentro del cluster que no sean secretos. Esto puede ayudar bastante a la hora de definir de manera separada a los 

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: special-config
  namespace: default
data:
  special.how: very
  special.type: charm
```

Despues de eso tan solo se pueden usarse usando `valueFrom` y `configMapKeyRef`, que permitira tomar el valor desde un `ConfigMap` que hayamos definido antes:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: dapi-test-pod
spec:
  containers:
    - name: test-container
      image: k8s.gcr.io/busybox
      command: [ "/bin/sh", "-c", "env" ]
      env:
        # Define the environment variable
        - name: SPECIAL_LEVEL_KEY
          valueFrom:
            configMapKeyRef:
              # The ConfigMap containing the value you want to assign to SPECIAL_LEVEL_KEY
              name: special-config
              # Specify the key associated with the value
              key: special.how
  restartPolicy: Never
```

### Imagenes en minikube

Podemos tener las imagenes ya creadas localmente:

```bash
$ docker images | grep cuando-viene
cuando-viene-paradas                                     latest               e9313b2cb524   26 minutes ago   120MB
cuando-viene-lineas                                      latest               f724ccda60b5   26 minutes ago   120MB
cuando-viene-monitoreo                                   latest               c868f3705c6f   26 minutes ago   120MB
cuando-viene-main                                        latest               5e0e72aed3c0   26 minutes ago   120MB
cuando-viene_paradas                                     latest               cf2910555155   33 minutes ago   120MB
cuando-viene_monitoreo                                   latest               51b3b9b1bb26   33 minutes ago   120MB
cuando-viene_main                                        latest               9778499ee06c   33 minutes ago   120MB
cuando-viene_lineas                                      latest               9a1b1407a796   33 minutes ago   120MB
```

El tema es que si levantamos el cluster, puede ser que los deployment que creemos en minikube tal vez no funcione bien y lo que nos devuelva es un tipo de error como `ImagePullBackOff`, esto es porque en vez de pullearse la imagen del entorno local o host, lo esta haciendo desde el reguistro de docker de [docker hub](https://hub.docker.com/).

Una alternativa simple, es tan solo el de subir las imagenes de nuestro entorno local a nuestra cuenta de docker hub creada. 

Otra alternativa es tratar de forzar el que traiga las imagenes de nuestro host local. Lo primero que hay que hacer es cambiar o agregar en la seccion de containers, la opcion de `imagePullPolicy` en `Never`

```yaml
...
    spec:
      containers:
        - image: nodejs-server
          name: nodejs-server
          imagePullPolicy: Never
```        

Si damos de baja el cluster con `kubectl delete -f nuestro_cluster.yaml`, y lo damos de nuevo de alta con `kubectl apply`, lo que nos va a resultar ahora es en el error `ErrImageNeverPull`

Si entramos en el cluster con `minikube ssh` y despues vemos las imagenes disponibles don `docker images`, nos va a devolver seguramente ninguna imagen. Esto es porque los demonios que tienen conexion con el registro local en nuestra maquina host y minikube son distintos.

Solucion...

Hay que ejecutar el siguiente comando para setear las variables de entorno y despues tratar de buildear de nuevo las imagenes de `cuando-viene` entonces hay que hacer:

- `eval $(minikube docker-env)`
- `./create_images`

Ahora deberiamos dar de baja el cluster y de nuevo de alta y listo!

## Notas sobre Deployments

En general no queremos describir pods y queremos trabajar con [deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/). Estos nos van a dar una manera un poco mas flexible de describir replica sets y de actualizar la configuracion y cambios que hagamos eventualmente con los pods que queremos describir. Esto puede ser porque en general, los pods no permiten facilmente actualizar parametro de la [seccion de .spec](https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md#spec-and-status). 

Con lo cual se usan otras abtracciones, entre ellas los deployments. Un ejemplo de un Deployment puede ser:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: servicio
  namespace: default
spec:
  replicas: 1
  selector:
    matchLabels:
      app: servicio
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 2
      maxUnavailable: 0
  template:
    metadata:
      labels:
        app: servicio
    spec:
      containers:
        - name: servicio
          image: blah/lalala:latest
          ports:
            - containerPort: 3000
          env:
            - name: MONGO_URL
              value: mongodb://mongo:27017/dev
          imagePullPolicy: Always
```

veamos de a poco las partes basicas de este simple deployment:

```yaml
metadata:
  name: servicio
  namespace: default
```

el name, permite describir el nombre y vamos a poder tambien decirle el namespace, si es que creamos uno, en donde estara el deployment y sus pods asociados

> Mas info desde `kubectl explain deployment.metadata`

despues esta el spec donde podremos definir el selector, que sera la manera que podremos despues saber y seleccionar este componente dentro del cluster.

Tambien podemos definir el tipo de [estrategia](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#strategy) que queremos de actualizacion, sea `RollingUpdate` o `Recreate`

```yaml
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 2
      maxUnavailable: 0
```      

en este caso al usar `RollingUpdate`, podemos definir la cantidad de pods de mas que podriamos llegar a tener en caso de actualizar el deployment con `maxSurge` y la maxima cantidad de pods que pueden estar no disponibles coon `maxUnavailable`. Una cosa a tener en cuenta es que `maxUnavailable` si es 0, entonces `maxSurge` no podra ser 0.

> Mas info haciendo `kubectl explain deployment.spec.strategy.rollingUpdate`

Tambien hay info sobre el [estado de los deployments aqui.](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#deployment-status)

Despues esta la parte mas importante en `spec.containers`

```yaml
    spec:
      containers:
        - name: servicio
          image: blah/lalala:latest
          ports:
            - containerPort: 3000
          env:
            - name: MONGO_URL
              value: mongodb://mongo:27017/dev
          imagePullPolicy: Always
```

Donde podemos ver el nombre que le damos a los containers, la imagen que tendra de base, el puerto que se expone, variables de entorno como `MONGO_UL`, y la politica de hacer el pull de la imagen.

Tambien hay otras cosas que se pueden definir como volumenes, recursos, probes y otro tipo de cosas y puede verse mas en detalle o bien [aqui](https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md#spec-and-status) o haciendo `kubectl explain deployment.spec.template.spec`

## Sobre los servicios

Cuando uno tiene listo los `Deployments` o `ReplicaSets` de uno o varios servicios, vamos a querer de alguna manera, poder o bien:

- Accederlos desde afuera
- Que puedan interconectarse

Como se logra esto???

La nocion de estos dos componentes que mencionamos es la describir los pods y sus configuraciones, pero no de como se accederan en la red, sea del cluster o que sean un nexo para comunicarse para afuera. Para describir este tipo de interacciones vamos a necesitar algo llamamo `Services`...

Los [servicios](https://kubernetes.io/docs/concepts/services-networking/service/) nos van a permitir este tipo de cosas y un ejemplo simple puede ser el siguiente:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  selector:
    app: MyDeployment
  ports:
    - protocol: TCP
      port: 80
      targetPort: 9376
```      

sobre la parte particular de:

```yaml
spec:
  selector:
    app: MyDeployment
```

es llamado el selector, y este va a tener que matchear con el label que le hayamos dado al `Deployment` o `ReplicaSet`, etc que hayamos creado antes, un ej puede ser:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: service
spec:
  # ...
  template:
    metadata:
      labels:
        app: MyDeployment
```

Tambien hay que definir el tipo de Servicio que queremos tener, si queremos que sea accedido solamente dentro del cluster, bastara con definirlo como `ClusterIP`, este es el valor por defecto, aunque podemos explicitarlo:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  type: ClusterIP
  selector:
    app: MyDeployment
  ports:
    - protocol: TCP
      name: internal
      port: 9376
      targetPort: 9376
```      

Otro tipo de servicio puede ser que sea accedido por afuera del cluster, en ese caso en general se usa el `type: LoadBalancer`:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service-ext
spec:
  type: LoadBalancer
  selector:
    app: MyDeployment
  ports:
    - protocol: TCP
      name: http
      port: 80
      targetPort: 9376
```

> Nota: Se puede ver mas de los tipos de servicios ejecutando `kubectl explain service.spec.type.`

Algo no menos importante es el `metadata.name`, que define como sera el hostname del servicio dentro del cluster, por lo que si queremos acceder al servicio `my-service:9376`, tendremos que tener el valor de `metadata.name` con ese mismo valor si o si:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
# ....
```

### Como puedo acceder a un servicio externo con minikube?

Haciendo algo como `kubectl get service -n <my namespace>`

```bash
$ kubectl get service -n cuando-viene
NAME                         TYPE           CLUSTER-IP       EXTERNAL-IP   PORT(S)        AGE
cuando-viene-monitoreo       ClusterIP      10.105.220.131   <none>        3003/TCP       78m
cuando-viene-monitoreo-ext   LoadBalancer   10.97.196.234    <pending>     80:30493/TCP   78m
mongodb                      ClusterIP      10.104.23.171    <none>        27017/TCP      171m
```

Para acceder u obtener el link del servicio de `cuando-viene-monitoreo-ext` hay que hacer:

```bash
$ minikube service cuando-viene-monitoreo-ext -n cuando-viene  --url
http://192.168.49.2:30493
```