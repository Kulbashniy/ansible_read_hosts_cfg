import sqlite3
import hashlib
from sql_params import _CHECK, _INSERT, _UPDATE, _HASH_FIND, _BUILD_FIND

class Sqlite_DB:
	def __init__(self, cfg_path):
		self.db_file = None
		path = ''
		name = ''
		with open(cfg_path, 'r') as f:
			for line in f:
				if line.find('db_path') != -1:
					path = line[8:]
					path = path.rstrip('\n')
				elif line.find('db_name') != -1:
					name = line[8:]
					name = name.rstrip('\n')
			self.db_file = path+'/'+name
		self.conn = sqlite3.connect(self.db_file)

	def insert(self, *args, **kwargs):
		cursor = self.conn.cursor()
		if len(args)!=0:
			hashstr = args[0]['project'] + args[0]['stage'] + args[0]['app'] + args[0]['verson']
			sha1 = hashlib.sha1(bytes(hashstr, 'utf-8')).hexdigest()
			cursor.execute(_INSERT, ('', args[0]['project'], args[0]['stage'], str(args[0]['time']), args[0]['app'], args[0]['verson'], str(args[0]['build']), sha1))
		else:
			hashstr = kwargs['project'] + kwargs['stage'] + kwargs['app'] + kwargs['verson']
			sha1 = hashlib.sha1(bytes(hashstr, 'utf-8')).hexdigest()
			cursor.execute(_INSERT, ('', kwargs['project'], kwargs['stage'], str(kwargs['time']), kwargs['app'], kwargs['verson'], str(kwargs['build']), sha1))
		self.conn.commit()

	def check(self, *args, **kwargs):
		cursor = self.conn.cursor()

		if len(args)!=0:
			cursor.execute(_CHECK, (args[0]['project'], args[0]['stage'], args[0]['app'], args[0]['verson'], str(args[0]['build'])))
		else:
			cursor.execute(_CHECK, (kwargs['project'], kwargs['stage'], kwargs['app'], kwargs['verson'], str(kwargs['build'])))

		rows = cursor.fetchall()
		if len(rows) == 0:
			return {'status': False, 'time': None}
		else:
			return {'status': True, 'time': rows[0][0]}

	def status(self, *args, **kwargs):
		if len(args)!=0:
			info = self.check(args[0])
		else:
			info = self.check(kwargs)
		if info['status']:
			if info['time'] == str(args[0]['time']):
				return 'ok'
			else:
				return 'update'
		else:
			return 'insert'

	def update(self, *args, **kwargs):
		cursor = self.conn.cursor()
		if len(args)!=0:
			cursor.execute(_UPDATE, (args[0]['time'], args[0]['project'], args[0]['stage'], args[0]['app'], args[0]['verson'], str(args[0]['build'])))
		else:
			cursor.execute(_UPDATE, (kwargs['time'], kwargs['project'], kwargs['stage'], kwargs['app'], kwargs['verson'], str(kwargs['build'])))
		self.conn.commit()

	def find_hash(self, sha1):
		cursor = self.conn.cursor()
		cursor.execute(_HASH_FIND, (sha1,))
		rows = cursor.fetchall()
		dict_list = dict({'assembly_list': list()})
		for record in rows:
			assembly_dict = {'project': record[1], 'stage': record[2], 'time': record[3], 'app': record[4], 'verson': record[5], 'build': record[6]}
			dict_list['assembly_list'].append(assembly_dict)
		return dict_list

	def find_build(self, *args, **kwargs):
		cursor = self.conn.cursor()
		if len(args)!=0:
			cursor.execute(_BUILD_FIND, (args[0][0], args[0][1]))
		else:
			cursor.execute(_BUILD_FIND, (kwargs['start'], kwargs['end']))
		rows = cursor.fetchall()
		dict_list = dict({'assembly_list': list()})
		for record in rows:
			assembly_dict = {'project': record[1], 'stage': record[2], 'time': record[3], 'app': record[4], 'verson': record[5], 'build': record[6]}
			dict_list['assembly_list'].append(assembly_dict)
		return dict_list


	def disconnect(self):
		self.conn.close()

	def open(self):
		self.conn = sqlite3.connect(self.db_file)