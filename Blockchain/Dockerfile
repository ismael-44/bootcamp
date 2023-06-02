FROM python
COPY exec.sh /exec.sh
RUN mkdir /jsons
COPY node* /jsons/
RUN apt update && apt install -y jq
CMD bash /exec.sh
