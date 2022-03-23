rm /home/pi/pcu/sqlite_database/pcu_database.db
cat /home/pi/pcu/sqlite_database/pcu_database.sql | sqlite3 /home/pi/pcu/sqlite_database/pcu_database.db
