# -*- coding: utf8 -*-
#user:gzf

#msg type could be REGISTER, UNREGISTER and HEARTBEAT
MSG_TYPE = 'TYPE'

#send register
REGISTER = 'REGISTER'

#unregister client with client_id assigned by master
UNREGISTER = 'UNREGISTER'

#send heart beat to server with client_id
HEARTBEAT = 'HEARTBEAT'

#notify master paused with client_id
PAUSED = 'PAUSED'

#notify master resumed with client_id
RESUMED = 'RESUMED'

#notify master shutdown with client_id
SHUTDOWN = 'SHUTDOWN'

#get a new location list to crawl
LOCATIONS = 'REQUIRE_LOCATION_LIST'

#get a new triple list to crawl
TRIPLES = 'TRIPLES'

DATA = 'DATA'

CRAWL_DELAY = 'CRAWL_DELAY'

#finished list of item
FINISHED_ITEMS = 'FINISHED_ITEMS'

#client id key word
CLIENT_ID = 'CLIENT_ID'

#server status key word
ACTION_REQUIRED = 'ACTION_REQUIRED'

#server require pause
PAUSE_REQUIRED = 'PAUSE_REQUIRED'

#server require resume
RESUME_REQUIRED = 'RESUME_REQUIRED'

# server require shutdown
SHUTDOWN_REQUIRED = 'SHUTDOWN_REQUIRED'

# server status key word
SERVER_STATUS = 'SERVER_STATUS'

# server status values
STATUS_RUNNING = 'STATUS_RUNNING'

STATUS_PAUSED  = 'STATUS_PAUSED'

STATUS_SHUTDOWN	= 'STATUS_SHUTDOWN'

STATUS_CONNECTION_LOST = 'STATUS_CONNECTION_LOST'

ERROR = 'ERROR'

# client id not found, then it needs to register itself
ERR_NOT_FOUND = 'ERR_NOT_FOUND'

REQUEST_SIZE = 10
CRAWL_DELAY_TIME = 2

