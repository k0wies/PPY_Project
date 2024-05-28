
--------------------------------------------------------
--  DDL for Table TODO_LIST
--------------------------------------------------------

-- Skrypt do Oracle SQL

  CREATE TABLE "TODO_LIST" 
   (	"ID" NUMBER(*,0), 
	"NAME" VARCHAR2(40 BYTE), 
	"DESCRIPTION" VARCHAR2(500 BYTE), 
	"CREATING_DATE" TIMESTAMP (6), 
	"STATUS" VARCHAR2(30 BYTE), 
	"TASK_PRIORITY" NUMBER(1,0)
   )

