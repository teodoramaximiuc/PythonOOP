
CREATE TABLE cliusers (
    id NUMBER(10) NOT NULL PRIMARY KEY,
    username VARCHAR2(50) NOT NULL,
    password VARCHAR2(100) NOT NULL
);
CREATE TABLE cliusers_audit (
    id NUMBER(10) NOT NULL PRIMARY KEY,
    userid NUMBER(10) NOT NULL REFERENCES cliusers(id),
    action VARCHAR2(50) NOT NULL,
    action_time DATE DEFAULT SYSDATE NOT NULL
);