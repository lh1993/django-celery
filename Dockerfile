FROM python:3.6
LABEL maintainer=lh mail=lhln0119@163.com

ENV PROD_PATH /app/DataCenter
ENV PROT 8080

RUN yum clean all &&\
    yum -y install mysql-devel wget net-tools make gcc gcc-c++ gcc-devel python3-devel libffi-devel libevent-devel which fontconfig mkfontscale libXrender* libXext* &&\
    mkdir -p $PROD_PATH/Data;\
    mkdir -p $PROD_PATH/DataCenter;\
    mkdir -p $PROD_PATH/ScheduleTasks;\
    mkdir -p $PROD_PATH/WeChat;\
    mkdir -p /app/config/ ;\
    sed -i 's/en_US/zh_CN/' /etc/locale.conf ;\
    localedef -c -f UTF-8 -i zh_CN zh_CN.UTF-8


COPY Data $PROD_PATH/Data/
COPY DataCenter $PROD_PATH/DataCenter/
COPY ScheduleTasks $PROD_PATH/ScheduleTasks/
COPY WeChat $PROD_PATH/WeChat/

COPY db.sqlite3 manage.py requirements.txt celerybeat-schedule run.sh $PROD_PATH/

RUN ls -la $PROD_PATH/* ;\
    cd $PROD_PATH ;\
    pip3 install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple;\
    pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 下载源码
RUN wget https://www.sqlite.org/2019/sqlite-autoconf-3290000.tar.gz ;\
    tar zxvf sqlite-autoconf-3290000.tar.gz ;\
    cd sqlite-autoconf-3290000/ ;\
    ./configure --prefix=/usr/local ;\
    make && make install ;\
    mv /usr/bin/sqlite3  /usr/bin/sqlite3_old ;\
    ln -s /usr/local/bin/sqlite3   /usr/bin/sqlite3 ;\
    echo "/usr/local/lib" > /etc/ld.so.conf.d/sqlite3.conf ;\
    ldconfig ;\
    sqlite3 -version
    

EXPOSE $PROT/tcp
WORKDIR $PROD_PATH

CMD [ "run.sh" ]
ENTRYPOINT [ "/bin/sh" ]
