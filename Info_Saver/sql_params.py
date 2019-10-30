_INSERT = """INSERT INTO 'projects' 
				('ip', 'project', 'stage', 'update_time', 'app', 'verson', 'build', 'sha1')
				VALUES (?,?,?,?,?,?,?,?);"""

_CHECK = """SELECT update_time FROM projects 
				WHERE project=? AND stage=? AND app=? AND verson=? AND build=?;"""

_UPDATE = """UPDATE projects SET update_time=? 
				WHERE project=? AND stage=? AND app=? AND verson=? AND build=?;"""

_HASH_FIND = "SELECT * FROM projects WHERE sha1=?;"

_BUILD_FIND = "SELECT * FROM projects WHERE build BETWEEN ? AND ? ORDER BY build;" 