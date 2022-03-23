
/* Create tables */

CREATE TABLE "record" (
    "id" INTEGER NOT NULL PRIMARY KEY,
    "record_datetime" DATETIME NOT NULL,
    "record_port_states" INTEGER NOT NULL
    );


CREATE TABLE "measure" (
    "id" INTEGER NOT NULL PRIMARY KEY,
    "record_id" INTEGER NOT NULL,
    "port_id" INTEGER NOT NULL,
    "current" REAL NOT NULL,
    "voltage" REAL NOT NULL,
    "power" REAL NOT NULL,
    FOREIGN KEY ("record_id") REFERENCES "record" ("id") ON DELETE CASCADE ON UPDATE CASCADE
    );

CREATE TABLE "bookkeepings" (
    "bk_name" TEXT PRIMARY KEY,
    "bk_value" INTEGER NOT NULL
     );

/* Create bookkeepings triggers */

CREATE TRIGGER record_limit_trigger BEFORE INSERT ON record
    FOR EACH ROW
    WHEN (SELECT bk_value FROM bookkeepings WHERE bk_name = 'Qty Entries')
    >= (SELECT bk_value FROM bookkeepings WHERE bk_name = 'Max Entries')
    BEGIN
        DELETE FROM record
          WHERE record_datetime = (SELECT record_datetime FROM record ORDER BY record_datetime LIMIT 1);
     END;

CREATE TRIGGER record_count_insert_trigger AFTER INSERT ON record
    FOR EACH ROW
    BEGIN
        UPDATE bookkeepings SET bk_value = bk_value + 1 WHERE bk_name = 'Qty Entries';
    END;

CREATE TRIGGER record_count_delete_trigger AFTER DELETE ON record
    FOR EACH ROW
    BEGIN
        UPDATE bookkeepings SET bk_value = bk_value - 1 WHERE bk_name = 'Qty Entries';
    END;

/* Set bookkeepings max entries */

INSERT INTO bookkeepings VALUES ('Max Entries', 172800);
INSERT INTO bookkeepings VALUES ('Qty Entries', 0);

