

# localdb base config

config = {
    'database': {
        'path': '/localdb/',# path should be exist,the root dir for localdb
        'tables':['header','bigchain','votes'], # the localdb dirs
        'block_size':None,# block size (in bytes)
        'write_buffer_size':2<<24,#  (int) – size of the write buffer (in bytes) 16MB *2 ?
        'max_open_files':None,# (int) – maximum number of files to keep open
        'lru_cache_size':None,# lru_cache_size (int) – size of the LRU cache (in bytes)
        'compression':'snappy',#  whether to use Snappy compression (enabled by default)

    },
    'encoding':'utf-8',# the encoding for bytes
}
