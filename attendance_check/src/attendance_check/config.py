### DB Connecion ###
mysql_config = {
	'host': '172.20.1.2', # HA Proxy IP
	'user': 'dbmanager',
	'pass': 'iris',
	'db': 'friday'
}

def get_alchemy_uri(mode='read'):
    port = 3307 if mode == 'read' else 3306 
    return 'mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8' % (
            mysql_config['user'], mysql_config['pass'], mysql_config['host'], port, mysql_config['db']
    )