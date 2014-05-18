DROP TABLE IF EXISTS "person";
CREATE TABLE "person" ("id" INTEGER NOT NULL PRIMARY KEY, "email" VARCHAR(255) NOT NULL, "password" VARCHAR(255) NOT NULL, "f_Name" VARCHAR(255) NOT NULL, "l_Name" VARCHAR(255) NOT NULL, "birthday" DATE NOT NULL);
INSERT INTO "person" VALUES(1,'e0','p0','user0','last0','2013-6-12');
INSERT INTO "person" VALUES(2,'e1','p1','Ali','Paul','2013-06-22');
INSERT INTO "person" VALUES(3,'e2','p2','user2','last2','2013-06-22');
INSERT INTO "person" VALUES(4,'','','','','');
INSERT INTO "person" VALUES(5,'e4','p4','user4','last4','2013-06-22');
INSERT INTO "person" VALUES(6,'1','3','4','5',2);
INSERT INTO "person" VALUES(7,'e6','p6','user6','last6','1/19/2000');
