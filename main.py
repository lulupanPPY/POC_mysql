import os

config = 'db_config'
sql_path = './sqls/'
dump_only_structure = True
mysqldump_path='/Applications/MySQLWorkbench.app/Contents/MacOS/'

def mysqldump(usr,pswd,host,port,db):
      print ('performe mysqldump for %s'%(db))
      if dump_only_structure:
            cmd = mysqldump_path+'mysqldump ' \
                  '--protocol=tcp --set-gtid-purged=OFF --default-character-set=utf8 --host=%s ' \
                  '--user=%s --password=%s --lock-tables=FALSE --add-locks=FALSE --port=%s --routines ' \
                  '--no-data --column-statistics=0 "%s"' \
                  ' > tmp.sql'%(host,usr,pswd,port,db)
      else:
            cmd = mysqldump_path+'mysqldump ' \
                  '--protocol=tcp --set-gtid-purged=OFF --default-character-set=utf8 --host=%s ' \
                  '--user=%s --password=%s --lock-tables=FALSE --add-locks=FALSE --port=%s --routines ' \
                  '--column-statistics=0 "%s"' \
                  ' > tmp.sql'%(host,usr,pswd,port,db)
      os.system(cmd)
      add_schema_DDL('tmp.sql',sql_path+db+'.sql',db)

def add_schema_DDL(file,dest,schema_name):
      create_schema = 'create database %s;'%(schema_name)
      use_schema = 'use %s;'%(schema_name)
      with open(file,'r') as f:
            with open(dest,'w') as w:
                  w.write(create_schema+'\n')
                  w.write(use_schema+'\n')
                  for l in f:
                        w.write(l+'\n')
      f.close()
      w.close()

def merge_files(path,dest):
      files = os.listdir(path)
      with open(dest,'w') as w:
            for f in files:
                  with open(path+f,'r') as sql:
                        for line in sql:
                              w.write(line+'\n')
                  sql.close()
            w.close()

if __name__ == '__main__':
      with open(config, 'r') as f:
            for l in f:
                  usr, pswd, host, port, db = l.split()
                  mysqldump(usr,pswd,host,port,db)
      merge_files(sql_path,'new_creditcore_all.sql')