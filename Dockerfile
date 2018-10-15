FROM python:3.6-alpine3.7

WORKDIR /src
COPY ./linear_solver ./linear_solver
COPY ./tests ./tests
COPY ./run_tests.sh ./run_tests.sh

RUN chmod +x ./run_tests.sh
CMD ["./run_tests.sh"]
