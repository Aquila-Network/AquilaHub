<div align="center">
  <a href="https://aquila.network">
    <img
      src="https://user-images.githubusercontent.com/19545678/133918727-5a37c6be-676f-427b-8c86-dd50f58d1287.png"
      alt="Aquila Network Logo"
      height="64"
    />
  </a>
  <br />
  <p>
    <h3>
      <b>
        Aquila Hub
      </b>
    </h3>
  </p>
  <p>
    <b>
      Load and serve Neural Encoder Models
    </b>
  </p>
  <br/>
</div>

Load and serve ML models to compress data into latent vectors. To be used with Aquila DB.

# Technology

Aquila Hub automates the process of encoding information with the help of ML models. Here is where Aquila Hub fits in the entire ecosystem:
<div align="center">
  <img
    src="https://user-images.githubusercontent.com/19545678/133918439-e08f314b-ad15-441e-a605-2fd2ec37a509.png"
    alt="Aquila Hub Architecture"
    height="400"
  />
 <br/>
</div>

# Install
### Debian

Run `curl -s -L https://raw.githubusercontent.com/Aquila-Network/AquilaHub/main/install.sh | /bin/bash -s -- -d 1 `.

### Docker

**You need docker installed in your system**

Build image (one time process): `docker build https://raw.githubusercontent.com/Aquila-Network/AquilaHub/main/Dockerfile -t aquilahub:local`

Run image (to deploy Aquila DB): `docker run -p 5002:5002 -d aquilahub:local`

# Client SDKs
We currently have multiple client libraries in progress to abstract the communication between deployed Aquila Hub and your applications.

[Python](https://github.com/Aquila-Network/AquilaPy)

[Node JS](https://github.com/Aquila-Network/AquilaJS)

## Where to get private key (wallet key) for client authentication
When you use a client library to authenticate with Aquila Hub, you might need access the same private key (wallet key) used by Aquila Hub. This key is located inside `/ossl/` directory within Aquila Hub docker container (in your computer if you have installed Aquila Hub directly without docker). To access the keys inside your Aquila Hub container, follow below steps:

* identify `CONTAINER ID` for the already running `aquilahub` docker instance:
`docker ps`
* take a copy of private keys from docker container to your host machine:
`docker cp CONTAINER_ID:/ossl/ ./`
* now you will see a new directory named `ossl` at your current location. Use the keys inside it.

#### tips for advanced users
If your pipeline requires the private keys to be generated in advance, you can do it in your host machine and then mount it to the container's `/ossl/` directory. 

Run:
```
mkdir -p <host>/ossl/
openssl genrsa -passout pass:1234 -des3 -out <host>/ossl/private.pem 2048
openssl rsa -passin pass:1234 -in <host>/ossl/private.pem -outform PEM -pubout -out <host>/ossl/public.pem
openssl rsa -passin pass:1234 -in <host>/ossl/private.pem -out <host>/ossl/private_unencrypted.pem -outform PEM
```
#### Note:
You can reuse the same keys across Aquila DB, Aquila Hub and Aquila Port.
