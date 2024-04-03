FROM crowdin/cli:3.19.2

RUN apk --no-cache add curl git jq gnupg;

COPY . .
COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
