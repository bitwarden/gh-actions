FROM mcr.microsoft.com/azure-cli:2.64.0

RUN yum -y install jq && yum -y clean all && rm -fr /var/cache 

COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]