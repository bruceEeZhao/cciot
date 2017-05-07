create database CCIOT;
use CCIOT;

create table IotUser 
(
U_id         int unsigned primary key,
U_name       varchar(20),
U_apikey     varchar(20) unique,
U_passwd     varchar(20),
U_email      varchar(50),
U_score      int unsigned,
U_level      int unsigned,
U_lasttime   datetime,
U_lastip     varchar(20)
);


create table IotDevice
(
D_id         int unsigned primary key,
D_name       varchar(20),
D_apikey     varchar(20) unique,
D_ifopen     tinyint unsigned,
D_status     tinyint unsigned,
D_oltime     int unsigned,
D_userid     int unsigned,
foreign key (D_userid) references IotUser (U_id)
);

create table IotControl
(
C_id         varchar(256) primary key,
C_time       datetime,
C_fid        int unsigned,
C_tid        int unsigned,
C_content    text
);

create table IotDataport
(
DP_id        int unsigned,
DP_deviceid  int unsigned,
DP_name      varchar(20),
DP_type      int unsigned,
DP_uptime    datetime,
primary key (DP_id, DP_deviceid),
foreign key (DP_deviceid) references IotDevice (D_id)
);

create table IotAlarmport
(
AP_id        int unsigned,
AP_portid    int unsigned,
AP_name      varchar(20),
AP_status    tinyint unsigned,
AP_method    int unsigned,
AP_condition text,
primary key (AP_id, AP_portid),
foreign key (AP_portid) references IotDataport (DP_id)
);
