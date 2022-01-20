# jaeger-example

## Set up local development environment

1. Install Python 3.8 and virtualenv
2. Change to the directory of your local clone of this repository

        cd ~/work/jaeger-example
3. Create python virtual environment

        python3 -m venv venv
4. Activate python virtual environment

        source env/bin/activate
5. Install required packages

        pip install -r requirements.txt

## Usage

### Run All-in-One Jaeger

_Mostly copied from [Jaeger Getting Started](https://www.jaegertracing.io/docs/1.30/getting-started/#all-in-one)._

      docker run -it --rm --name jaeger \
      -e COLLECTOR_ZIPKIN_HOST_PORT=:9411 \
      -p 5775:5775/udp \
      -p 6831:6831/udp \
      -p 6832:6832/udp \
      -p 5778:5778 \
      -p 16686:16686 \
      -p 14250:14250 \
      -p 14268:14268 \
      -p 14269:14269 \
      -p 9411:9411 \
      jaegertracing/all-in-one:1.30

View the Jaeger UI at [http://localhost:16686](http://localhost:16686) .

## Run jaeger-example locally

    source env/bin/activate
    export SOMETHING=something
    python app.py

### Swagger Docs

http://localhost:8000/docs
