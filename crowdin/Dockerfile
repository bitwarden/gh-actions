FROM crowdin/cli:3.16.0

RUN apk --no-cache add curl git jq gnupg;

COPY . .
COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
