rm /home/pi/pcu/sqlite_database/record_database.db
rm /home/pi/pcu/sqlite_database/port_database.db
cat /home/pi/pcu/sqlite_database/record_database.sql | sqlite3 /home/pi/pcu/sqlite_database/record_database.db
cat /home/pi/pcu/sqlite_database/port_database.sql | sqlite3 /home/pi/pcu/sqlite_database/port_database.db
