import codecs, os, random, string, sys, time

from pkg import six



VERSION = "0.1.1.4"
TYPE = "dev" if VERSION.count('.') > 2 and VERSION.split('.')[-1] != '0' else "stable"
TYPE_COLORS = {"dev": 33, "stable": 90, "pip": 34}
VERSION_STRING = "Ankabut/%s#%s" % ('.'.join(VERSION.split('.')[:-1]) if VERSION.count('.') > 2 and VERSION.split('.')[-1] == '0' else VERSION, TYPE)
DESCRIPTION = "automatic SQL injection and database takeover tool"
SITE = "https://github.com"
DEFAULT_USER_AGENT = "%s (%s)" % (VERSION_STRING, SITE)
DEV_EMAIL_ADDRESS = "dev@Ankabut.org"
ISSUES_PAGE = "https://github.com/AiAnsar1/Ankabut/issues/new"
GIT_REPOSITORY = "https://github.com/AiAnsar1/Ankabut.git"
GIT_PAGE = "https://github.com/AiAnsar1/Ankabut"
WIKI_PAGE = "https://github.com/AiAnsar1/Ankabut/wiki/"
ZIPBALL_PAGE = "https://github.com/AiAnsar1/Ankabut/master"



BANNER = """\033[01;33m\
        ___
       __H__
 ___ ___[.]_____ ___ ___  \033[01;37m{\033[01;%dm%s\033[01;37m}\033[01;33m
|_ -| . [.]     | .'| . |
|___|_  [.]_|_|_|__,|  _|
      |_|V...       |_|   \033[0m\033[4;37m%s\033[0m\n
""" % (TYPE_COLORS.get(TYPE, 31), VERSION_STRING.split('/')[-1], SITE)



DIFF_TOLERANCE = 0.05
CONSTANT_RATIO = 0.9

# Ratio used in heuristic check for WAF/IPS protected targets
IPS_WAF_CHECK_RATIO = 0.5

# Timeout used in heuristic check for WAF/IPS protected targets
IPS_WAF_CHECK_TIMEOUT = 10

# Timeout used in checking for existence of live-cookies file
LIVE_COOKIES_TIMEOUT = 120

# Lower and upper values for match ratio in case of stable page
LOWER_RATIO_BOUND = 0.02
UPPER_RATIO_BOUND = 0.98

# For filling in case of dumb push updates
DUMMY_JUNK = "ahy9Ouge"

# Markers for special cases when parameter values contain html encoded characters
PARAMETER_AMP_MARKER = "__AMP__"
PARAMETER_SEMICOLON_MARKER = "__SEMICOLON__"
BOUNDARY_BACKSLASH_MARKER = "__BACKSLASH__"
PARAMETER_PERCENTAGE_MARKER = "__PERCENTAGE__"
PARTIAL_VALUE_MARKER = "__PARTIAL_VALUE__"
PARTIAL_HEX_VALUE_MARKER = "__PARTIAL_HEX_VALUE__"
URI_QUESTION_MARKER = "__QUESTION__"
ASTERISK_MARKER = "__ASTERISK__"
REPLACEMENT_MARKER = "__REPLACEMENT__"
BOUNDED_BASE64_MARKER = "__BOUNDED_BASE64__"
BOUNDED_INJECTION_MARKER = "__BOUNDED_INJECTION__"
SAFE_VARIABLE_MARKER = "__SAFE__"
SAFE_HEX_MARKER = "__SAFE_HEX__"
DOLLAR_MARKER = "__DOLLAR__"

RANDOM_INTEGER_MARKER = "[RANDINT]"
RANDOM_STRING_MARKER = "[RANDSTR]"
SLEEP_TIME_MARKER = "[SLEEPTIME]"
INFERENCE_MARKER = "[INFERENCE]"
SINGLE_QUOTE_MARKER = "[SINGLE_QUOTE]"
GENERIC_SQL_COMMENT_MARKER = "[GENERIC_SQL_COMMENT]"

PAYLOAD_DELIMITER = "__PAYLOAD_DELIMITER__"
CHAR_INFERENCE_MARK = "%c"
PRINTABLE_CHAR_REGEX = r"[^\x00-\x1f\x7f-\xff]"

# Regular expression used for extraction of table names (useful for (e.g.) MsAccess)
SELECT_FROM_TABLE_REGEX = r"\bSELECT\b.+?\bFROM\s+(?P<result>([\w.]|`[^`<>]+`)+)"

# Regular expression used for recognition of textual content-type
TEXT_CONTENT_TYPE_REGEX = r"(?i)(text|form|message|xml|javascript|ecmascript|json)"

# Regular expression used for recognition of generic permission messages
PERMISSION_DENIED_REGEX = r"(?P<result>(command|permission|access)\s*(was|is)?\s*denied)"

# Regular expression used in recognition of generic protection mechanisms
GENERIC_PROTECTION_REGEX = r"(?i)\b(rejected|blocked|protection|incident|denied|detected|dangerous|firewall)\b"

# Regular expression used to detect errors in fuzz(y) UNION test
FUZZ_UNION_ERROR_REGEX = r"(?i)data\s?type|comparable|compatible|conversion|converting|failed|error"

# Upper threshold for starting the fuzz(y) UNION test
FUZZ_UNION_MAX_COLUMNS = 10

# Regular expression used for recognition of generic maximum connection messages
MAX_CONNECTIONS_REGEX = r"\bmax.{1,100}\bconnection"

# Maximum consecutive connection errors before asking the user if he wants to continue
MAX_CONSECUTIVE_CONNECTION_ERRORS = 15

# Timeout before the pre-connection candidate is being disposed (because of high probability that the web server will reset it)
PRECONNECT_CANDIDATE_TIMEOUT = 10

# Servers known to cause issue with pre-connection mechanism (because of lack of multi-threaded support)
PRECONNECT_INCOMPATIBLE_SERVERS = ("SimpleHTTP", "BaseHTTP")

# Identify WAF/IPS inside limited number of responses (Note: for optimization purposes)
IDENTYWAF_PARSE_LIMIT = 10

# Maximum sleep time in "Murphy" (testing) mode
MAX_MURPHY_SLEEP_TIME = 3

# Regular expression used for extracting results from Google search
GOOGLE_REGEX = r"webcache\.googleusercontent\.com/search\?q=cache:[^:]+:([^+]+)\+&amp;cd=|url\?\w+=((?![^>]+webcache\.googleusercontent\.com)http[^>]+)&(sa=U|rct=j)"

# Google Search consent cookie
GOOGLE_CONSENT_COOKIE = "CONSENT=YES+shp.gws-%s-0-RC1.%s+FX+740" % (time.strftime("%Y%m%d"), "".join(random.sample(string.ascii_lowercase, 2)))

# Regular expression used for extracting results from DuckDuckGo search
DUCKDUCKGO_REGEX = r'<a class="result__url" href="(htt[^"]+)'

# Regular expression used for extracting results from Bing search
BING_REGEX = r'<h2><a href="([^"]+)" h='

# Dummy user agent for search (if default one returns different results)
DUMMY_SEARCH_USER_AGENT = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0"

# Regular expression used for extracting content from "textual" tags
TEXT_TAG_REGEX = r"(?si)<(abbr|acronym|b|blockquote|br|center|cite|code|dt|em|font|h\d|i|li|p|pre|q|strong|sub|sup|td|th|title|tt|u)(?!\w).*?>(?P<result>[^<]+)"

# Regular expression used for recognition of IP addresses
IP_ADDRESS_REGEX = r"\b(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\b"

# Regular expression used for recognition of generic "your ip has been blocked" messages
BLOCKED_IP_REGEX = r"(?i)(\A|\b)ip\b.*\b(banned|blocked|block list|firewall)"

# Dumping characters used in GROUP_CONCAT MySQL technique
CONCAT_ROW_DELIMITER = ','
CONCAT_VALUE_DELIMITER = '|'

# Coefficient used for a time-based query delay checking (must be >= 7)
TIME_STDEV_COEFF = 7

# Minimum response time that can be even considered as delayed (not a complete requirement)
MIN_VALID_DELAYED_RESPONSE = 0.5

# Standard deviation after which a warning message should be displayed about connection lags
WARN_TIME_STDEV = 0.5

# Minimum length of usable union injected response (quick defense against substr fields)
UNION_MIN_RESPONSE_CHARS = 10

# Coefficient used for a union-based number of columns checking (must be >= 7)
UNION_STDEV_COEFF = 7

# Length of queue for candidates for time delay adjustment
TIME_DELAY_CANDIDATES = 3

# Default value for HTTP Accept header
HTTP_ACCEPT_HEADER_VALUE = "*/*"

# Default value for HTTP Accept-Encoding header
HTTP_ACCEPT_ENCODING_HEADER_VALUE = "gzip,deflate"

# Default timeout for running commands over backdoor
BACKDOOR_RUN_CMD_TIMEOUT = 5

# Number of seconds to wait for thread finalization at program end
THREAD_FINALIZATION_TIMEOUT = 1

# Maximum number of techniques used in inject.py/getValue() per one value
MAX_TECHNIQUES_PER_VALUE = 2

# In case of missing piece of partial union dump, buffered array must be flushed after certain size
MAX_BUFFERED_PARTIAL_UNION_LENGTH = 1024

# Maximum size of cache used in @cachedmethod decorator
MAX_CACHE_ITEMS = 256

# Suffix used for naming meta databases in DBMS(es) without explicit database name
METADB_SUFFIX = "_masterdb"

# Number of times to retry the pushValue during the exceptions (e.g. KeyboardInterrupt)
PUSH_VALUE_EXCEPTION_RETRY_COUNT = 3

# Minimum time response set needed for time-comparison based on standard deviation
MIN_TIME_RESPONSES = 30

# Maximum time response set used during time-comparison based on standard deviation
MAX_TIME_RESPONSES = 200

# Minimum comparison ratio set needed for searching valid union column number based on standard deviation
MIN_UNION_RESPONSES = 5

# After these number of blanks at the end inference should stop (just in case)
INFERENCE_BLANK_BREAK = 5

# Use this replacement character for cases when inference is not able to retrieve the proper character value
INFERENCE_UNKNOWN_CHAR = '?'

# Character used for operation "greater" in inference
INFERENCE_GREATER_CHAR = ">"

# Character used for operation "greater or equal" in inference
INFERENCE_GREATER_EQUALS_CHAR = ">="

# Character used for operation "equals" in inference
INFERENCE_EQUALS_CHAR = "="

# Character used for operation "not-equals" in inference
INFERENCE_NOT_EQUALS_CHAR = "!="

# String used for representation of unknown DBMS
UNKNOWN_DBMS = "Unknown"

# String used for representation of unknown DBMS version
UNKNOWN_DBMS_VERSION = "Unknown"

# Dynamicity boundary length used in dynamicity removal engine
DYNAMICITY_BOUNDARY_LENGTH = 20

# Dummy user prefix used in dictionary attack
DUMMY_USER_PREFIX = "__dummy__"

# Reference: http://en.wikipedia.org/wiki/ISO/IEC_8859-1
DEFAULT_PAGE_ENCODING = "iso-8859-1"

try:
    codecs.lookup(DEFAULT_PAGE_ENCODING)
except LookupError:
    DEFAULT_PAGE_ENCODING = "utf8"

# Marker for program piped input
STDIN_PIPE_DASH = '-'

# URL used in dummy runs
DUMMY_URL = "http://foo/bar?id=1"

# Timeout used during initial websocket (pull) testing
WEBSOCKET_INITIAL_TIMEOUT = 3

# The name of the operating system dependent module imported. The following names have currently been registered: 'posix', 'nt', 'mac', 'os2', 'ce', 'java', 'riscos'
PLATFORM = os.name
PYVERSION = sys.version.split()[0]
IS_WIN = PLATFORM == "nt"

# Check if running in terminal
IS_TTY = hasattr(sys.stdout, "fileno") and os.isatty(sys.stdout.fileno())

# DBMS system databases
MSSQL_SYSTEM_DBS = ("Northwind", "master", "model", "msdb", "pubs", "tempdb", "Resource", "ReportServer", "ReportServerTempDB")
MYSQL_SYSTEM_DBS = ("information_schema", "mysql", "performance_schema", "sys")
PGSQL_SYSTEM_DBS = ("information_schema", "pg_catalog", "pg_toast", "pgagent")
ORACLE_SYSTEM_DBS = ("ADAMS", "ANONYMOUS", "APEX_030200", "APEX_PUBLIC_USER", "APPQOSSYS", "AURORA$ORB$UNAUTHENTICATED", "AWR_STAGE", "BI", "BLAKE", "CLARK", "CSMIG", "CTXSYS", "DBSNMP", "DEMO", "DIP", "DMSYS", "DSSYS", "EXFSYS", "FLOWS_%", "FLOWS_FILES", "HR", "IX", "JONES", "LBACSYS", "MDDATA", "MDSYS", "MGMT_VIEW", "OC", "OE", "OLAPSYS", "ORACLE_OCM", "ORDDATA", "ORDPLUGINS", "ORDSYS", "OUTLN", "OWBSYS", "PAPER", "PERFSTAT", "PM", "SCOTT", "SH", "SI_INFORMTN_SCHEMA", "SPATIAL_CSW_ADMIN_USR", "SPATIAL_WFS_ADMIN_USR", "SYS", "SYSMAN", "SYSTEM", "TRACESVR", "TSMSYS", "WK_TEST", "WKPROXY", "WKSYS", "WMSYS", "XDB", "XS$NULL")
SQLITE_SYSTEM_DBS = ("sqlite_master", "sqlite_temp_master")
ACCESS_SYSTEM_DBS = ("MSysAccessObjects", "MSysACEs", "MSysObjects", "MSysQueries", "MSysRelationships", "MSysAccessStorage", "MSysAccessXML", "MSysModules", "MSysModules2")
FIREBIRD_SYSTEM_DBS = ("RDB$BACKUP_HISTORY", "RDB$CHARACTER_SETS", "RDB$CHECK_CONSTRAINTS", "RDB$COLLATIONS", "RDB$DATABASE", "RDB$DEPENDENCIES", "RDB$EXCEPTIONS", "RDB$FIELDS", "RDB$FIELD_DIMENSIONS", " RDB$FILES", "RDB$FILTERS", "RDB$FORMATS", "RDB$FUNCTIONS", "RDB$FUNCTION_ARGUMENTS", "RDB$GENERATORS", "RDB$INDEX_SEGMENTS", "RDB$INDICES", "RDB$LOG_FILES", "RDB$PAGES", "RDB$PROCEDURES", "RDB$PROCEDURE_PARAMETERS", "RDB$REF_CONSTRAINTS", "RDB$RELATIONS", "RDB$RELATION_CONSTRAINTS", "RDB$RELATION_FIELDS", "RDB$ROLES", "RDB$SECURITY_CLASSES", "RDB$TRANSACTIONS", "RDB$TRIGGERS", "RDB$TRIGGER_MESSAGES", "RDB$TYPES", "RDB$USER_PRIVILEGES", "RDB$VIEW_RELATIONS")
MAXDB_SYSTEM_DBS = ("SYSINFO", "DOMAIN")
SYBASE_SYSTEM_DBS = ("master", "model", "sybsystemdb", "sybsystemprocs")
DB2_SYSTEM_DBS = ("NULLID", "SQLJ", "SYSCAT", "SYSFUN", "SYSIBM", "SYSIBMADM", "SYSIBMINTERNAL", "SYSIBMTS", "SYSPROC", "SYSPUBLIC", "SYSSTAT", "SYSTOOLS")
HSQLDB_SYSTEM_DBS = ("INFORMATION_SCHEMA", "SYSTEM_LOB")
H2_SYSTEM_DBS = ("INFORMATION_SCHEMA",) + ("IGNITE", "ignite-sys-cache")
INFORMIX_SYSTEM_DBS = ("sysmaster", "sysutils", "sysuser", "sysadmin")
MONETDB_SYSTEM_DBS = ("tmp", "json", "profiler")
DERBY_SYSTEM_DBS = ("NULLID", "SQLJ", "SYS", "SYSCAT", "SYSCS_DIAG", "SYSCS_UTIL", "SYSFUN", "SYSIBM", "SYSPROC", "SYSSTAT")
VERTICA_SYSTEM_DBS = ("v_catalog", "v_internal", "v_monitor",)
MCKOI_SYSTEM_DBS = ("",)
PRESTO_SYSTEM_DBS = ("information_schema",)
ALTIBASE_SYSTEM_DBS = ("SYSTEM_",)
MIMERSQL_SYSTEM_DBS = ("information_schema", "SYSTEM",)
CRATEDB_SYSTEM_DBS = ("information_schema", "pg_catalog", "sys")
CLICKHOUSE_SYSTEM_DBS = ("information_schema", "INFORMATION_SCHEMA", "system")
CUBRID_SYSTEM_DBS = ("DBA",)
CACHE_SYSTEM_DBS = ("%Dictionary", "INFORMATION_SCHEMA", "%SYS")
EXTREMEDB_SYSTEM_DBS = ("",)
FRONTBASE_SYSTEM_DBS = ("DEFINITION_SCHEMA", "INFORMATION_SCHEMA")
RAIMA_SYSTEM_DBS = ("",)
VIRTUOSO_SYSTEM_DBS = ("",)

# Note: (<regular>) + (<forks>)
MSSQL_ALIASES = ("microsoft sql server", "mssqlserver", "mssql", "ms")
MYSQL_ALIASES = ("mysql", "my") + ("mariadb", "maria", "memsql", "tidb", "percona", "drizzle")
PGSQL_ALIASES = ("postgresql", "postgres", "pgsql", "psql", "pg") + ("cockroach", "cockroachdb", "amazon redshift", "redshift", "greenplum", "yellowbrick", "enterprisedb", "yugabyte", "yugabytedb", "opengauss")
ORACLE_ALIASES = ("oracle", "orcl", "ora", "or")
SQLITE_ALIASES = ("sqlite", "sqlite3")
ACCESS_ALIASES = ("microsoft access", "msaccess", "access", "jet")
FIREBIRD_ALIASES = ("firebird", "mozilla firebird", "interbase", "ibase", "fb")
MAXDB_ALIASES = ("max", "maxdb", "sap maxdb", "sap db")
SYBASE_ALIASES = ("sybase", "sybase sql server")
DB2_ALIASES = ("db2", "ibm db2", "ibmdb2")
HSQLDB_ALIASES = ("hsql", "hsqldb", "hs", "hypersql")
H2_ALIASES = ("h2",) + ("ignite", "apache ignite")
INFORMIX_ALIASES = ("informix", "ibm informix", "ibminformix")
MONETDB_ALIASES = ("monet", "monetdb",)
DERBY_ALIASES = ("derby", "apache derby",)
VERTICA_ALIASES = ("vertica",)
MCKOI_ALIASES = ("mckoi",)
PRESTO_ALIASES = ("presto",)
ALTIBASE_ALIASES = ("altibase",)
MIMERSQL_ALIASES = ("mimersql", "mimer")
CRATEDB_ALIASES = ("cratedb", "crate")
CUBRID_ALIASES = ("cubrid",)
CLICKHOUSE_ALIASES = ("clickhouse",)
CACHE_ALIASES = ("intersystems cache", "cachedb", "cache", "iris")
EXTREMEDB_ALIASES = ("extremedb", "extreme")
FRONTBASE_ALIASES = ("frontbase",)
RAIMA_ALIASES = ("raima database manager", "raima", "raimadb", "raimadm", "rdm", "rds", "velocis")
VIRTUOSO_ALIASES = ("virtuoso", "openlink virtuoso")

DBMS_DIRECTORY_DICT = dict((getattr(DBMS, _), getattr(DBMS_DIRECTORY_NAME, _)) for _ in dir(DBMS) if not _.startswith("_"))

SUPPORTED_DBMS = set(MSSQL_ALIASES + MYSQL_ALIASES + PGSQL_ALIASES + ORACLE_ALIASES + SQLITE_ALIASES + ACCESS_ALIASES + FIREBIRD_ALIASES + MAXDB_ALIASES + SYBASE_ALIASES + DB2_ALIASES + HSQLDB_ALIASES + H2_ALIASES + INFORMIX_ALIASES + MONETDB_ALIASES + DERBY_ALIASES + VERTICA_ALIASES + MCKOI_ALIASES + PRESTO_ALIASES + ALTIBASE_ALIASES + MIMERSQL_ALIASES + CLICKHOUSE_ALIASES + CRATEDB_ALIASES + CUBRID_ALIASES + CACHE_ALIASES + EXTREMEDB_ALIASES + RAIMA_ALIASES + VIRTUOSO_ALIASES)
SUPPORTED_OS = ("linux", "windows")

DBMS_ALIASES = ((DBMS.MSSQL, MSSQL_ALIASES), (DBMS.MYSQL, MYSQL_ALIASES), (DBMS.PGSQL, PGSQL_ALIASES), (DBMS.ORACLE, ORACLE_ALIASES), (DBMS.SQLITE, SQLITE_ALIASES), (DBMS.ACCESS, ACCESS_ALIASES), (DBMS.FIREBIRD, FIREBIRD_ALIASES), (DBMS.MAXDB, MAXDB_ALIASES), (DBMS.SYBASE, SYBASE_ALIASES), (DBMS.DB2, DB2_ALIASES), (DBMS.HSQLDB, HSQLDB_ALIASES), (DBMS.H2, H2_ALIASES), (DBMS.INFORMIX, INFORMIX_ALIASES), (DBMS.MONETDB, MONETDB_ALIASES), (DBMS.DERBY, DERBY_ALIASES), (DBMS.VERTICA, VERTICA_ALIASES), (DBMS.MCKOI, MCKOI_ALIASES), (DBMS.PRESTO, PRESTO_ALIASES), (DBMS.ALTIBASE, ALTIBASE_ALIASES), (DBMS.MIMERSQL, MIMERSQL_ALIASES), (DBMS.CLICKHOUSE, CLICKHOUSE_ALIASES), (DBMS.CRATEDB, CRATEDB_ALIASES), (DBMS.CUBRID, CUBRID_ALIASES), (DBMS.CACHE, CACHE_ALIASES), (DBMS.EXTREMEDB, EXTREMEDB_ALIASES), (DBMS.FRONTBASE, FRONTBASE_ALIASES), (DBMS.RAIMA, RAIMA_ALIASES), (DBMS.VIRTUOSO, VIRTUOSO_ALIASES))

USER_AGENT_ALIASES = ("ua", "useragent", "user-agent")
REFERER_ALIASES = ("ref", "referer", "referrer")
HOST_ALIASES = ("host",)

# DBMSes with upper case identifiers
UPPER_CASE_DBMSES = set((DBMS.ORACLE, DBMS.DB2, DBMS.FIREBIRD, DBMS.MAXDB, DBMS.H2, DBMS.HSQLDB, DBMS.DERBY, DBMS.ALTIBASE))

# Default schemas to use (when unable to enumerate)
H2_DEFAULT_SCHEMA = HSQLDB_DEFAULT_SCHEMA = "PUBLIC"
VERTICA_DEFAULT_SCHEMA = "public"
MCKOI_DEFAULT_SCHEMA = "APP"
CACHE_DEFAULT_SCHEMA = "SQLUser"

# DBMSes where OFFSET mechanism starts from 1
PLUS_ONE_DBMSES = set((DBMS.ORACLE, DBMS.DB2, DBMS.ALTIBASE, DBMS.MSSQL, DBMS.CACHE))

# Names that can't be used to name files on Windows OS
WINDOWS_RESERVED_NAMES = ("CON", "PRN", "AUX", "NUL", "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9", "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9")

# Items displayed in basic help (-h) output
BASIC_HELP_ITEMS = (
    "url",
    "googleDork",
    "data",
    "cookie",
    "randomAgent",
    "proxy",
    "testParameter",
    "dbms",
    "level",
    "risk",
    "technique",
    "getAll",
    "getBanner",
    "getCurrentUser",
    "getCurrentDb",
    "getPasswordHashes",
    "getDbs",
    "getTables",
    "getColumns",
    "getSchema",
    "dumpTable",
    "dumpAll",
    "db",
    "tbl",
    "col",
    "osShell",
    "osPwn",
    "batch",
    "checkTor",
    "flushSession",
    "tor",
    "AnkabutShell",
    "wizard",
)

# Tags used for value replacements inside shell scripts
SHELL_WRITABLE_DIR_TAG = "%WRITABLE_DIR%"
SHELL_RUNCMD_EXE_TAG = "%RUNCMD_EXE%"

# String representation for NULL value
NULL = "NULL"

# String representation for blank ('') value
BLANK = "<blank>"

# String representation for current database
CURRENT_DB = "CD"

# String representation for current user
CURRENT_USER = "CU"

# Name of SQLite file used for storing session data
SESSION_SQLITE_FILE = "session.sqlite"

# Regular expressions used for finding file paths in error messages
FILE_PATH_REGEXES = (r"<b>(?P<result>[^<>]+?)</b> on line \d+", r"\bin (?P<result>[^<>'\"]+?)['\"]? on line \d+", r"(?:[>(\[\s])(?P<result>[A-Za-z]:[\\/][\w. \\/-]*)", r"(?:[>(\[\s])(?P<result>/\w[/\w.~-]+)", r"\bhref=['\"]file://(?P<result>/[^'\"]+)", r"\bin <b>(?P<result>[^<]+): line \d+")

# Regular expressions used for parsing error messages (--parse-errors)
ERROR_PARSING_REGEXES = (
    r"\[Microsoft\]\[ODBC SQL Server Driver\]\[SQL Server\](?P<result>[^<]+)",
    r"<b>[^<]{0,100}(fatal|error|warning|exception)[^<]*</b>:?\s*(?P<result>[^<]+)",
    r"(?m)^\s{0,100}(fatal|error|warning|exception):?\s*(?P<result>[^\n]+?)$",
    r"(sql|dbc)[^>'\"]{0,32}(fatal|error|warning|exception)(</b>)?:\s*(?P<result>[^<>]+)",
    r"(?P<result>[^\n>]{0,100}SQL Syntax[^\n<]+)",
    r"(?s)<li>Error Type:<br>(?P<result>.+?)</li>",
    r"CDbCommand (?P<result>[^<>\n]*SQL[^<>\n]+)",
    r"Code: \d+. DB::Exception: (?P<result>[^<>\n]*)",
    r"error '[0-9a-f]{8}'((<[^>]+>)|\s)+(?P<result>[^<>]+)",
    r"\[[^\n\]]{1,100}(ODBC|JDBC)[^\n\]]+\](\[[^\]]+\])?(?P<result>[^\n]+(in query expression|\(SQL| at /[^ ]+pdo)[^\n<]+)",
    r"(?P<result>query error: SELECT[^<>]+)"
)

# Regular expression used for parsing charset info from meta html headers
META_CHARSET_REGEX = r'(?si)<head>.*<meta[^>]+charset="?(?P<result>[^"> ]+).*</head>'

# Regular expression used for parsing refresh info from meta html headers
META_REFRESH_REGEX = r'(?i)<meta http-equiv="?refresh"?[^>]+content="?[^">]+;\s*(url=)?["\']?(?P<result>[^\'">]+)'

# Regular expression used for parsing Javascript redirect request
JAVASCRIPT_HREF_REGEX = r'<script>\s*(\w+\.)?location\.href\s*=["\'](?P<result>[^"\']+)'

# Regular expression used for parsing empty fields in tested form data
EMPTY_FORM_FIELDS_REGEX = r'(&|\A)(?P<result>[^=]+=)(?=&|\Z)'

# Reference: http://www.cs.ru.nl/bachelorscripties/2010/Martin_Devillers___0437999___Analyzing_password_strength.pdf
COMMON_PASSWORD_SUFFIXES = ("1", "123", "2", "12", "3", "13", "7", "11", "5", "22", "23", "01", "4", "07", "21", "14", "10", "06", "08", "8", "15", "69", "16", "6", "18")

# Reference: http://www.the-interweb.com/serendipity/index.php?/archives/94-A-brief-analysis-of-40,000-leaked-MySpace-passwords.html
COMMON_PASSWORD_SUFFIXES += ("!", ".", "*", "!!", "?", ";", "..", "!!!", ", ", "@")

# Splitter used between requests in WebScarab log files
WEBSCARAB_SPLITTER = "### Conversation"

# Splitter used between requests in BURP log files
BURP_REQUEST_REGEX = r"={10,}\s+([A-Z]{3,} .+?)\s+(={10,}|\Z)"

# Regex used for parsing XML Burp saved history items
BURP_XML_HISTORY_REGEX = r'<port>(\d+)</port>.*?<request base64="true"><!\[CDATA\[([^]]+)'

# Encoding used for Unicode data
UNICODE_ENCODING = "utf8"

# Reference: http://www.w3.org/Protocols/HTTP/Object_Headers.html#uri
URI_HTTP_HEADER = "URI"

# Uri format which could be injectable (e.g. www.site.com/id82)
URI_INJECTABLE_REGEX = r"//[^/]*/([^\.*?]+)\Z"

# Regex used for masking sensitive data
SENSITIVE_DATA_REGEX = r"(\s|=)(?P<result>[^\s=]*\b%s\b[^\s]*)\s"

# Options to explicitly mask in anonymous (unhandled exception) reports (along with anything carrying the <hostname> inside)
SENSITIVE_OPTIONS = ("hostname", "answers", "data", "dnsDomain", "googleDork", "authCred", "proxyCred", "tbl", "db", "col", "user", "cookie", "proxy", "fileRead", "fileWrite", "fileDest", "testParameter", "authCred", "sqlQuery", "requestFile", "csrfToken", "csrfData", "csrfUrl", "testParameter")

# Maximum number of threads (avoiding connection issues and/or DoS)
MAX_NUMBER_OF_THREADS = 10

# Minimum range between minimum and maximum of statistical set
MIN_STATISTICAL_RANGE = 0.01

# Minimum value for comparison ratio
MIN_RATIO = 0.0

# Maximum value for comparison ratio
MAX_RATIO = 1.0

# Minimum length of sentence for automatic choosing of --string (in case of high matching ratio)
CANDIDATE_SENTENCE_MIN_LENGTH = 10

# Character used for marking injectable position inside provided data
CUSTOM_INJECTION_MARK_CHAR = '*'

# Wildcard value that can be used in option --ignore-code
IGNORE_CODE_WILDCARD = '*'

# Other way to declare injection position
INJECT_HERE_REGEX = r"(?i)%INJECT[_ ]?HERE%"

# Minimum chunk length used for retrieving data over error based payloads
MIN_ERROR_CHUNK_LENGTH = 8

# Maximum chunk length used for retrieving data over error based payloads
MAX_ERROR_CHUNK_LENGTH = 1024

# Do not escape the injected statement if it contains any of the following SQL keywords
EXCLUDE_UNESCAPE = ("WAITFOR DELAY '", " INTO DUMPFILE ", " INTO OUTFILE ", "CREATE ", "BULK ", "EXEC ", "RECONFIGURE ", "DECLARE ", "'%s'" % CHAR_INFERENCE_MARK)

# Mark used for replacement of reflected values
REFLECTED_VALUE_MARKER = "__REFLECTED_VALUE__"

# Regular expression used for replacing border non-alphanum characters
REFLECTED_BORDER_REGEX = r"[^A-Za-z]+"

# Regular expression used for replacing non-alphanum characters
REFLECTED_REPLACEMENT_REGEX = r"[^\n]{1,168}"

# Maximum time (in seconds) spent per reflective value(s) replacement
REFLECTED_REPLACEMENT_TIMEOUT = 3

# Maximum number of alpha-numerical parts in reflected regex (for speed purposes)
REFLECTED_MAX_REGEX_PARTS = 10

# Chars which can be used as a failsafe values in case of too long URL encoding value
URLENCODE_FAILSAFE_CHARS = "()|,"

# Factor used for yuge page multiplication
YUGE_FACTOR = 1000

# Maximum length of URL encoded value after which failsafe procedure takes away
URLENCODE_CHAR_LIMIT = 2000

# Default schema for Microsoft SQL Server DBMS
DEFAULT_MSSQL_SCHEMA = "dbo"

# Display hash attack info every mod number of items
HASH_MOD_ITEM_DISPLAY = 11

# Display marker for (cracked) empty password
HASH_EMPTY_PASSWORD_MARKER = "<empty>"

# Maximum integer value
MAX_INT = sys.maxsize

# Replacement for unsafe characters in dump table filenames
UNSAFE_DUMP_FILEPATH_REPLACEMENT = '_'

# Options that need to be restored in multiple targets run mode
RESTORE_MERGED_OPTIONS = ("col", "db", "dnsDomain", "privEsc", "tbl", "regexp", "string", "textOnly", "threads", "timeSec", "tmpPath", "uChar", "user")

# Parameters to be ignored in detection phase (upper case)
IGNORE_PARAMETERS = ("__VIEWSTATE", "__VIEWSTATEENCRYPTED", "__VIEWSTATEGENERATOR", "__EVENTARGUMENT", "__EVENTTARGET", "__EVENTVALIDATION", "ASPSESSIONID", "ASP.NET_SESSIONID", "JSESSIONID", "CFID", "CFTOKEN")

# Regular expression used for recognition of ASP.NET control parameters
ASP_NET_CONTROL_REGEX = r"(?i)\Actl\d+\$"

# Regex for Google analytics cookie names
GOOGLE_ANALYTICS_COOKIE_REGEX = r"(?i)\A(__utm|_ga|_gid|_gat|_gcl_au)"

# Prefix for configuration overriding environment variables
ANKABUT_ENVIRONMENT_PREFIX = "ANKABUT_"

# General OS environment variables that can be used for setting proxy address
PROXY_ENVIRONMENT_VARIABLES = ("all_proxy", "ALL_PROXY", "http_proxy", "HTTP_PROXY", "https_proxy", "HTTPS_PROXY")

# Turn off resume console info to avoid potential slowdowns
TURN_OFF_RESUME_INFO_LIMIT = 20

# Strftime format for results file used in multiple target mode
RESULTS_FILE_FORMAT = "results-%m%d%Y_%I%M%p.csv"

# Official web page with the list of Python supported codecs
CODECS_LIST_PAGE = "http://docs.python.org/library/codecs.html#standard-encodings"

# Simple regular expression used to distinguish scalar from multiple-row commands (not sole condition)
SQL_SCALAR_REGEX = r"\A(SELECT(?!\s+DISTINCT\(?))?\s*\w*\("

# Option/switch values to ignore during configuration save
IGNORE_SAVE_OPTIONS = ("saveConfig",)

# IP address of the localhost
LOCALHOST = "127.0.0.1"

# Default SOCKS ports used by Tor
DEFAULT_TOR_SOCKS_PORTS = (9050, 9150)

# Default HTTP ports used by Tor
DEFAULT_TOR_HTTP_PORTS = (8123, 8118)

# Percentage below which comparison engine could have problems
LOW_TEXT_PERCENT = 20

# Auxiliary value used in isDBMSVersionAtLeast() version comparison correction cases
VERSION_COMPARISON_CORRECTION = 0.0001

# These MySQL keywords can't go (alone) into versioned comment form (/*!...*/)
# Reference: http://dev.mysql.com/doc/refman/5.1/en/function-resolution.html
IGNORE_SPACE_AFFECTED_KEYWORDS = ("CAST", "COUNT", "EXTRACT", "GROUP_CONCAT", "MAX", "MID", "MIN", "SESSION_USER", "SUBSTR", "SUBSTRING", "SUM", "SYSTEM_USER", "TRIM")

# Keywords expected to be in UPPERCASE in getValue()
GET_VALUE_UPPERCASE_KEYWORDS = ("SELECT", "FROM", "WHERE", "DISTINCT", "COUNT")

LEGAL_DISCLAIMER = "Usage of ANKABUT for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program"

# After this number of misses reflective removal mechanism is turned off (for speed up reasons)
REFLECTIVE_MISS_THRESHOLD = 20

# Regular expression used for extracting HTML title
HTML_TITLE_REGEX = r"(?i)<title>(?P<result>[^<]+)</title>"

# Table used for Base64 conversion in WordPress hash cracking routine
ITOA64 = "./0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

# Options/switches to be ignored in command-line parsing (e.g. those passed from Firefox)
IGNORED_OPTIONS = ("--compressed",)

# Chars used to quickly distinguish if the user provided tainted parameter values
DUMMY_SQL_INJECTION_CHARS = ";()'"

# Simple check against dummy users
DUMMY_USER_INJECTION = r"(?i)[^\w](AND|OR)\s+[^\s]+[=><]|\bUNION\b.+\bSELECT\b|\bSELECT\b.+\bFROM\b|\b(CONCAT|information_schema|SLEEP|DELAY|FLOOR\(RAND)\b"

# Extensions skipped by crawler
CRAWL_EXCLUDE_EXTENSIONS = ("3ds", "3g2", "3gp", "7z", "DS_Store", "a", "aac", "adp", "ai", "aif", "aiff", "apk", "ar", "asf", "au", "avi", "bak", "bin", "bk", "bmp", "btif", "bz2", "cab", "caf", "cgm", "cmx", "cpio", "cr2", "dat", "deb", "djvu", "dll", "dmg", "dmp", "dng", "doc", "docx", "dot", "dotx", "dra", "dsk", "dts", "dtshd", "dvb", "dwg", "dxf", "ear", "ecelp4800", "ecelp7470", "ecelp9600", "egg", "eol", "eot", "epub", "exe", "f4v", "fbs", "fh", "fla", "flac", "fli", "flv", "fpx", "fst", "fvt", "g3", "gif", "gz", "h261", "h263", "h264", "ico", "ief", "image", "img", "ipa", "iso", "jar", "jpeg", "jpg", "jpgv", "jpm", "jxr", "ktx", "lvp", "lz", "lzma", "lzo", "m3u", "m4a", "m4v", "mar", "mdi", "mid", "mj2", "mka", "mkv", "mmr", "mng", "mov", "movie", "mp3", "mp4", "mp4a", "mpeg", "mpg", "mpga", "mxu", "nef", "npx", "o", "oga", "ogg", "ogv", "otf", "pbm", "pcx", "pdf", "pea", "pgm", "pic", "png", "pnm", "ppm", "pps", "ppt", "pptx", "ps", "psd", "pya", "pyc", "pyo", "pyv", "qt", "rar", "ras", "raw", "rgb", "rip", "rlc", "rz", "s3m", "s7z", "scm", "scpt", "sgi", "shar", "sil", "smv", "so", "sub", "swf", "tar", "tbz2", "tga", "tgz", "tif", "tiff", "tlz", "ts", "ttf", "uvh", "uvi", "uvm", "uvp", "uvs", "uvu", "viv", "vob", "war", "wav", "wax", "wbmp", "wdp", "weba", "webm", "webp", "whl", "wm", "wma", "wmv", "wmx", "woff", "woff2", "wvx", "xbm", "xif", "xls", "xlsx", "xlt", "xm", "xpi", "xpm", "xwd", "xz", "z", "zip", "zipx")

# Patterns often seen in HTTP headers containing custom injection marking character '*'
PROBLEMATIC_CUSTOM_INJECTION_PATTERNS = r"(;q=[^;']+)|(\*/\*)"

# Template used for common table existence check
BRUTE_TABLE_EXISTS_TEMPLATE = "EXISTS(SELECT %d FROM %s)"

# Template used for common column existence check
BRUTE_COLUMN_EXISTS_TEMPLATE = "EXISTS(SELECT %s FROM %s)"

# Data inside shellcodeexec to be filled with random string
SHELLCODEEXEC_RANDOM_STRING_MARKER = b"XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

# Period after last-update to start nagging about the old revision
LAST_UPDATE_NAGGING_DAYS = 180

# Minimum non-writing chars (e.g. ['"-:/]) ratio in case of parsed error messages
MIN_ERROR_PARSING_NON_WRITING_RATIO = 0.05

# Generic address for checking the Internet connection while using switch --check-internet (Note: https version does not work for Python < 2.7.9)
CHECK_INTERNET_ADDRESS = "http://ipinfo.io/json"

# Value to look for in response to CHECK_INTERNET_ADDRESS
CHECK_INTERNET_VALUE = '"ip":'

# Payload used for checking of existence of WAF/IPS (dummier the better)
IPS_WAF_CHECK_PAYLOAD = "AND 1=1 UNION ALL SELECT 1,NULL,'<script>alert(\"XSS\")</script>',table_name FROM information_schema.tables WHERE 2>1--/**/; EXEC xp_cmdshell('cat ../../../etc/passwd')#"

# Vectors used for provoking specific WAF/IPS behavior(s)
WAF_ATTACK_VECTORS = (
    "",  # NIL
    "search=<script>alert(1)</script>",
    "file=../../../../etc/passwd",
    "q=<invalid>foobar",
    "id=1 %s" % IPS_WAF_CHECK_PAYLOAD
)

# Used for status representation in dictionary attack phase
ROTATING_CHARS = ('\\', '|', '|', '/', '-')

# Approximate chunk length (in bytes) used by BigArray objects (only last chunk and cached one are held in memory)
BIGARRAY_CHUNK_SIZE = 1024 * 1024

# Compress level used for storing BigArray chunks to disk (0-9)
BIGARRAY_COMPRESS_LEVEL = 9

# Maximum number of socket pre-connects
SOCKET_PRE_CONNECT_QUEUE_SIZE = 3

# Only console display last n table rows
TRIM_STDOUT_DUMP_SIZE = 256

# Reference: http://stackoverflow.com/a/3168436
# Reference: https://web.archive.org/web/20150407141500/https://support.microsoft.com/en-us/kb/899149
DUMP_FILE_BUFFER_SIZE = 1024

# Parse response headers only first couple of times
PARSE_HEADERS_LIMIT = 3

# Step used in ORDER BY technique used for finding the right number of columns in UNION query injections
ORDER_BY_STEP = 10

# Maximum value used in ORDER BY technique used for finding the right number of columns in UNION query injections
ORDER_BY_MAX = 1000

# Maximum number of times for revalidation of a character in inference (as required)
MAX_REVALIDATION_STEPS = 5

# Characters that can be used to split parameter values in provided command line (e.g. in --tamper)
PARAMETER_SPLITTING_REGEX = r"[,|;]"

# Attribute used for storing original parameter value in special cases (e.g. POST)
UNENCODED_ORIGINAL_VALUE = "original"

# Common column names containing usernames (used for hash cracking in some cases)
COMMON_USER_COLUMNS = ("login", "user", "username", "user_name", "user_login", "account", "account_name", "benutzername", "benutzer", "utilisateur", "usager", "consommateur", "utente", "utilizzatore", "utilizator", "utilizador", "usufrutuario", "korisnik", "uporabnik", "usuario", "consumidor", "client", "customer", "cuser")

# Default delimiter in GET/POST values
DEFAULT_GET_POST_DELIMITER = '&'

# Default delimiter in cookie values
DEFAULT_COOKIE_DELIMITER = ';'

# Unix timestamp used for forcing cookie expiration when provided with --load-cookies
FORCE_COOKIE_EXPIRATION_TIME = "9999999999"

# Github OAuth token used for creating an automatic Issue for unhandled exceptions
GITHUB_REPORT_OAUTH_TOKEN = "wxqc7vTeW8ohIcX+1wK55Mnql2Ex9cP+2s1dqTr/mjlZJVfLnq24fMAi08v5vRvOmuhVZQdOT/lhIRovWvIJrdECD1ud8VMPWpxY+NmjHoEx+VLK1/vCAUBwJe"

# Skip unforced HashDB flush requests below the threshold number of cached items
HASHDB_FLUSH_THRESHOLD = 32

# Number of retries for unsuccessful HashDB flush attempts
HASHDB_FLUSH_RETRIES = 3

# Number of retries for unsuccessful HashDB retrieve attempts
HASHDB_RETRIEVE_RETRIES = 3

# Number of retries for unsuccessful HashDB end transaction attempts
HASHDB_END_TRANSACTION_RETRIES = 3

# Unique milestone value used for forced deprecation of old HashDB values (e.g. when changing hash/pickle mechanism)
HASHDB_MILESTONE_VALUE = "OdqjeUpBLc"  # python -c 'import random, string; print "".join(random.sample(string.ascii_letters, 10))'

# Pickle protocl used for storage of serialized data inside HashDB (https://docs.python.org/3/library/pickle.html#data-stream-format)
PICKLE_PROTOCOL = 2

# Warn user of possible delay due to large page dump in full UNION query injections
LARGE_OUTPUT_THRESHOLD = 1024 ** 2

# On huge tables there is a considerable slowdown if every row retrieval requires ORDER BY (most noticable in table dumping using ERROR injections)
SLOW_ORDER_COUNT_THRESHOLD = 10000

# Give up on hash recognition if nothing was found in first given number of rows
HASH_RECOGNITION_QUIT_THRESHOLD = 1000

# Regular expression used for automatic hex conversion and hash cracking of (RAW) binary column values
HASH_BINARY_COLUMNS_REGEX = r"(?i)pass|psw|hash"

# Maximum number of redirections to any single URL - this is needed because of the state that cookies introduce
MAX_SINGLE_URL_REDIRECTIONS = 4

# Maximum total number of redirections (regardless of URL) - before assuming we're in a loop
MAX_TOTAL_REDIRECTIONS = 10

# Maximum (deliberate) delay used in page stability check
MAX_STABILITY_DELAY = 0.5

# Reference: http://www.tcpipguide.com/free/t_DNSLabelsNamesandSyntaxRules.htm
MAX_DNS_LABEL = 63

# Alphabet used for prefix and suffix strings of name resolution requests in DNS technique (excluding hexadecimal chars for not mixing with inner content)
DNS_BOUNDARIES_ALPHABET = re.sub(r"[a-fA-F]", "", string.ascii_letters)

# Alphabet used for heuristic checks
HEURISTIC_CHECK_ALPHABET = ('"', '\'', ')', '(', ',', '.')

# Minor artistic touch
BANNER = re.sub(r"\[.\]", lambda _: "[\033[01;41m%s\033[01;49m]" % random.sample(HEURISTIC_CHECK_ALPHABET, 1)[0], BANNER)

# String used for dummy non-SQLi (e.g. XSS) heuristic checks of a tested parameter value
DUMMY_NON_SQLI_CHECK_APPENDIX = "<'\">"

# Regular expression used for recognition of file inclusion errors
FI_ERROR_REGEX = r"(?i)[^\n]{0,100}(no such file|failed (to )?open)[^\n]{0,100}"

# Length of prefix and suffix used in non-SQLI heuristic checks
NON_SQLI_CHECK_PREFIX_SUFFIX_LENGTH = 6

# Connection read size (processing large responses in parts to avoid MemoryError crashes - e.g. large table dump in full UNION injections)
MAX_CONNECTION_READ_SIZE = 10 * 1024 * 1024

# Maximum response total page size (trimmed if larger)
MAX_CONNECTION_TOTAL_SIZE = 100 * 1024 * 1024

# For preventing MemoryError exceptions (caused when using large sequences in difflib.SequenceMatcher)
MAX_DIFFLIB_SEQUENCE_LENGTH = 10 * 1024 * 1024

# Page size threshold used in heuristic checks (e.g. getHeuristicCharEncoding(), identYwaf, htmlParser, etc.)
HEURISTIC_PAGE_SIZE_THRESHOLD = 64 * 1024

# Maximum (multi-threaded) length of entry in bisection algorithm
MAX_BISECTION_LENGTH = 50 * 1024 * 1024

# Mark used for trimming unnecessary content in large connection reads
LARGE_READ_TRIM_MARKER = "__TRIMMED_CONTENT__"

# Generic SQL comment formation
GENERIC_SQL_COMMENT = "-- [RANDSTR]"

# Threshold value for turning back on time auto-adjustment mechanism
VALID_TIME_CHARS_RUN_THRESHOLD = 100

# Check for empty columns only if table is sufficiently large
CHECK_ZERO_COLUMNS_THRESHOLD = 10

# Boldify all logger messages containing these "patterns"
BOLD_PATTERNS = ("' injectable", "provided empty", "leftover chars", "might be injectable", "' is vulnerable", "is not injectable", "does not seem to be", "test failed", "test passed", "live test final result", "test shows that", "the back-end DBMS is", "created Github", "blocked by the target server", "protection is involved", "CAPTCHA", "specific response", "NULL connection is supported", "PASSED", "FAILED", "for more than", "connection to ")

# TLDs used in randomization of email-alike parameter values
RANDOMIZATION_TLDS = ("com", "net", "ru", "org", "de", "uk", "br", "jp", "cn", "fr", "it", "pl", "tv", "edu", "in", "ir", "es", "me", "info", "gr", "gov", "ca", "co", "se", "cz", "to", "vn", "nl", "cc", "az", "hu", "ua", "be", "no", "biz", "io", "ch", "ro", "sk", "eu", "us", "tw", "pt", "fi", "at", "lt", "kz", "cl", "hr", "pk", "lv", "la", "pe", "au")

# Generic www root directory names
GENERIC_DOC_ROOT_DIRECTORY_NAMES = ("htdocs", "httpdocs", "public", "public_html", "wwwroot", "www", "site")

# Maximum length of a help part containing switch/option name(s)
MAX_HELP_OPTION_LENGTH = 18

# Maximum number of connection retries (to prevent problems with recursion)
MAX_CONNECT_RETRIES = 100

# Strings for detecting formatting errors
FORMAT_EXCEPTION_STRINGS = ("Type mismatch", "Error converting", "Please enter a", "Conversion failed", "String or binary data would be truncated", "Failed to convert", "unable to interpret text value", "Input string was not in a correct format", "System.FormatException", "java.lang.NumberFormatException", "ValueError: invalid literal", "TypeMismatchException", "CF_SQL_INTEGER", "CF_SQL_NUMERIC", " for CFSQLTYPE ", "cfqueryparam cfsqltype", "InvalidParamTypeException", "Invalid parameter type", "Attribute validation error for tag", "is not of type numeric", "<cfif Not IsNumeric(", "invalid input syntax for integer", "invalid input syntax for type", "invalid number", "character to number conversion error", "unable to interpret text value", "String was not recognized as a valid", "Convert.ToInt", "cannot be converted to a ", "InvalidDataException", "Arguments are of the wrong type", "Invalid conversion")

# Regular expression used for extracting ASP.NET view state values
VIEWSTATE_REGEX = r'(?i)(?P<name>__VIEWSTATE[^"]*)[^>]+value="(?P<result>[^"]+)'

# Regular expression used for extracting ASP.NET event validation values
EVENTVALIDATION_REGEX = r'(?i)(?P<name>__EVENTVALIDATION[^"]*)[^>]+value="(?P<result>[^"]+)'

# Number of rows to generate inside the full union test for limited output (mustn't be too large to prevent payload length problems)
LIMITED_ROWS_TEST_NUMBER = 15

# Default adapter to use for bottle server
RESTAPI_DEFAULT_ADAPTER = "wsgiref"

# Default REST-JSON API server listen address
RESTAPI_DEFAULT_ADDRESS = "127.0.0.1"

# Default REST-JSON API server listen port
RESTAPI_DEFAULT_PORT = 8775

# Unsupported options by REST-JSON API server
RESTAPI_UNSUPPORTED_OPTIONS = ("sqlShell", "wizard")

# Use "Supplementary Private Use Area-A"
INVALID_UNICODE_PRIVATE_AREA = False

# Format used for representing invalid unicode characters
INVALID_UNICODE_CHAR_FORMAT = r"\x%02x"

# Minimum supported version of httpx library (for --http2)
MIN_HTTPX_VERSION = "0.28"

# Regular expression for XML POST data
XML_RECOGNITION_REGEX = r"(?s)\A\s*<[^>]+>(.+>)?\s*\Z"

# Regular expression used for detecting JSON POST data
JSON_RECOGNITION_REGEX = r'(?s)\A(\s*\[)*\s*\{.*"[^"]+"\s*:\s*("[^"]*"|\d+|true|false|null|\[).*\}\s*(\]\s*)*\Z'

# Regular expression used for detecting JSON-like POST data
JSON_LIKE_RECOGNITION_REGEX = r"(?s)\A(\s*\[)*\s*\{.*('[^']+'|\"[^\"]+\"|\w+)\s*:\s*('[^']+'|\"[^\"]+\"|\d+).*\}\s*(\]\s*)*\Z"

# Regular expression used for detecting multipart POST data
MULTIPART_RECOGNITION_REGEX = r"(?i)Content-Disposition:[^;]+;\s*name="

# Regular expression used for detecting Array-like POST data
ARRAY_LIKE_RECOGNITION_REGEX = r"(\A|%s)(\w+)\[\d*\]=.+%s\2\[\d*\]=" % (DEFAULT_GET_POST_DELIMITER, DEFAULT_GET_POST_DELIMITER)

# Default POST data content-type
DEFAULT_CONTENT_TYPE = "application/x-www-form-urlencoded; charset=utf-8"

# Raw text POST data content-type
PLAIN_TEXT_CONTENT_TYPE = "text/plain; charset=utf-8"

# Length used while checking for existence of Suhosin-patch (like) protection mechanism
SUHOSIN_MAX_VALUE_LENGTH = 512

# Minimum size of an (binary) entry before it can be considered for dumping to disk
MIN_BINARY_DISK_DUMP_SIZE = 100

# Filenames of payloads xml files (in order of loading)
PAYLOAD_XML_FILES = ("boolean_blind.xml", "error_based.xml", "inline_query.xml", "stacked_queries.xml", "time_blind.xml", "union_query.xml")

# Regular expression used for extracting form tags
FORM_SEARCH_REGEX = r"(?si)<form(?!.+<form).+?</form>"

# Maximum number of lines to save in history file
MAX_HISTORY_LENGTH = 1000

# Minimum field entry length needed for encoded content (hex, base64,...) check
MIN_ENCODED_LEN_CHECK = 5

# Timeout in seconds in which Metasploit remote session has to be initialized
METASPLOIT_SESSION_TIMEOUT = 120

# Reference: http://www.postgresql.org/docs/9.0/static/catalog-pg-largeobject.html
LOBLKSIZE = 2048

# Prefix used to mark special variables (e.g. keywords, having special chars, etc.)
EVALCODE_ENCODED_PREFIX = "EVAL_"

# Reference: https://en.wikipedia.org/wiki/Zip_(file_format)
ZIP_HEADER = b"\x50\x4b\x03\x04"

# Reference: http://www.cookiecentral.com/faq/#3.5
NETSCAPE_FORMAT_HEADER_COOKIES = "# Netscape HTTP Cookie File."

# Infixes used for automatic recognition of parameters carrying anti-CSRF tokens
CSRF_TOKEN_PARAMETER_INFIXES = ("csrf", "xsrf", "token")

# Prefixes used in brute force search for web server document root
BRUTE_DOC_ROOT_PREFIXES = {
    OS.LINUX: ("/var/www", "/usr/local/apache", "/usr/local/apache2", "/usr/local/www/apache22", "/usr/local/www/apache24", "/usr/local/httpd", "/var/www/nginx-default", "/srv/www", "/var/www/%TARGET%", "/var/www/vhosts/%TARGET%", "/var/www/virtual/%TARGET%", "/var/www/clients/vhosts/%TARGET%", "/var/www/clients/virtual/%TARGET%"),
    OS.WINDOWS: ("/xampp", "/Program Files/xampp", "/wamp", "/Program Files/wampp", "/Apache/Apache", "/apache", "/Program Files/Apache Group/Apache", "/Program Files/Apache Group/Apache2", "/Program Files/Apache Group/Apache2.2", "/Program Files/Apache Group/Apache2.4", "/Inetpub/wwwroot", "/Inetpub/wwwroot/%TARGET%", "/Inetpub/vhosts/%TARGET%")
}

# Suffixes used in brute force search for web server document root
BRUTE_DOC_ROOT_SUFFIXES = ("", "html", "htdocs", "httpdocs", "php", "public", "src", "site", "build", "web", "www", "data", "sites/all", "www/build")

# String used for marking target name inside used brute force web server document root
BRUTE_DOC_ROOT_TARGET_MARK = "%TARGET%"

# Character used as a boundary in kb.chars (preferably less frequent letter)
KB_CHARS_BOUNDARY_CHAR = 'q'

# Letters of lower frequency used in kb.chars
KB_CHARS_LOW_FREQUENCY_ALPHABET = "zqxjkvbp"

# Printable bytes
PRINTABLE_BYTES = set(bytes(string.printable, "ascii") if six.PY3 else string.printable)

# SQL keywords used for splitting in HTTP chunked transfer encoded requests (switch --chunk)
HTTP_CHUNKED_SPLIT_KEYWORDS = ("SELECT", "UPDATE", "INSERT", "FROM", "LOAD_FILE", "UNION", "information_schema", "sysdatabases", "msysaccessobjects", "msysqueries", "sysmodules")

# CSS style used in HTML dump format
HTML_DUMP_CSS_STYLE = """<style>
table{
    margin:10;
    background-color:#FFFFFF;
    font-family:verdana;
    font-size:12px;
    align:center;
}
thead{
    font-weight:bold;
    background-color:#4F81BD;
    color:#FFFFFF;
}
tr:nth-child(even) {
    background-color: #D3DFEE
}
td{
    font-size:12px;
}
th{
    font-size:12px;
}
</style>"""




FIREBIRD_TYPES = {
    261: "BLOB",
    14: "CHAR",
    40: "CSTRING",
    11: "D_FLOAT",
    27: "DOUBLE",
    10: "FLOAT",
    16: "INT64",
    8: "INTEGER",
    9: "QUAD",
    7: "SMALLINT",
    12: "DATE",
    13: "TIME",
    35: "TIMESTAMP",
    37: "VARCHAR",
}

INFORMIX_TYPES = {
    0: "CHAR",
    1: "SMALLINT",
    2: "INTEGER",
    3: "FLOAT",
    4: "SMALLFLOAT",
    5: "DECIMAL",
    6: "SERIAL",
    7: "DATE",
    8: "MONEY",
    9: "NULL",
    10: "DATETIME",
    11: "BYTE",
    12: "TEXT",
    13: "VARCHAR",
    14: "INTERVAL",
    15: "NCHAR",
    16: "NVARCHAR",
    17: "INT8",
    18: "SERIAL8",
    19: "SET",
    20: "MULTISET",
    21: "LIST",
    22: "ROW (unnamed)",
    23: "COLLECTION",
    40: "Variable-length opaque type",
    41: "Fixed-length opaque type",
    43: "LVARCHAR",
    45: "BOOLEAN",
    52: "BIGINT",
    53: "BIGSERIAL",
    2061: "IDSSECURITYLABEL",
    4118: "ROW (named)",
}

SYBASE_TYPES = {
    14: "floatn",
    8: "float",
    15: "datetimn",
    12: "datetime",
    23: "real",
    28: "numericn",
    10: "numeric",
    27: "decimaln",
    26: "decimal",
    17: "moneyn",
    11: "money",
    21: "smallmoney",
    22: "smalldatetime",
    13: "intn",
    7: "int",
    6: "smallint",
    5: "tinyint",
    16: "bit",
    2: "varchar",
    18: "sysname",
    25: "nvarchar",
    1: "char",
    24: "nchar",
    4: "varbinary",
    80: "timestamp",
    3: "binary",
    19: "text",
    20: "image",
}

ALTIBASE_TYPES = {
    1: "CHAR",
    12: "VARCHAR",
    -8: "NCHAR",
    -9: "NVARCHAR",
    2: "NUMERIC",
    6: "FLOAT",
    8: "DOUBLE",
    7: "REAL",
    -5: "BIGINT",
    4: "INTEGER",
    5: "SMALLINT",
    9: "DATE",
    30: "BLOB",
    40: "CLOB",
    20001: "BYTE",
    20002: "NIBBLE",
    -7: "BIT",
    -100: "VARBIT",
    10003: "GEOMETRY",
}

MYSQL_PRIVS = {
    1: "select_priv",
    2: "insert_priv",
    3: "update_priv",
    4: "delete_priv",
    5: "create_priv",
    6: "drop_priv",
    7: "reload_priv",
    8: "shutdown_priv",
    9: "process_priv",
    10: "file_priv",
    11: "grant_priv",
    12: "references_priv",
    13: "index_priv",
    14: "alter_priv",
    15: "show_db_priv",
    16: "super_priv",
    17: "create_tmp_table_priv",
    18: "lock_tables_priv",
    19: "execute_priv",
    20: "repl_slave_priv",
    21: "repl_client_priv",
    22: "create_view_priv",
    23: "show_view_priv",
    24: "create_routine_priv",
    25: "alter_routine_priv",
    26: "create_user_priv",
}

PGSQL_PRIVS = {
    1: "createdb",
    2: "super",
    3: "catupd",
}

# Reference(s): http://stackoverflow.com/a/17672504
#               http://docwiki.embarcadero.com/InterBase/XE7/en/RDB$USER_PRIVILEGES

FIREBIRD_PRIVS = {
    "S": "SELECT",
    "I": "INSERT",
    "U": "UPDATE",
    "D": "DELETE",
    "R": "REFERENCE",
    "X": "EXECUTE",
    "A": "ALL",
    "M": "MEMBER",
    "T": "DECRYPT",
    "E": "ENCRYPT",
    "B": "SUBSCRIBE",
}

# Reference(s): https://www.ibm.com/support/knowledgecenter/SSGU8G_12.1.0/com.ibm.sqls.doc/ids_sqs_0147.htm
#               https://www.ibm.com/support/knowledgecenter/SSGU8G_11.70.0/com.ibm.sqlr.doc/ids_sqr_077.htm

INFORMIX_PRIVS = {
    "D": "DBA (all privileges)",
    "R": "RESOURCE (create UDRs, UDTs, permanent tables and indexes)",
    "C": "CONNECT (work with existing tables)",
    "G": "ROLE",
    "U": "DEFAULT (implicit connection)",
}

DB2_PRIVS = {
    1: "CONTROLAUTH",
    2: "ALTERAUTH",
    3: "DELETEAUTH",
    4: "INDEXAUTH",
    5: "INSERTAUTH",
    6: "REFAUTH",
    7: "SELECTAUTH",
    8: "UPDATEAUTH",
}

DUMP_REPLACEMENTS = {" ": NULL, "": BLANK}

DBMS_DICT = {
    DBMS.MSSQL: (MSSQL_ALIASES, "python-pymssql", "https://github.com/pymssql/pymssql", "mssql+pymssql"),
    DBMS.MYSQL: (MYSQL_ALIASES, "python-pymysql", "https://github.com/PyMySQL/PyMySQL", "mysql"),
    DBMS.PGSQL: (PGSQL_ALIASES, "python-psycopg2", "https://github.com/psycopg/psycopg2", "postgresql"),
    DBMS.ORACLE: (ORACLE_ALIASES, "python cx_Oracle", "https://oracle.github.io/python-cx_Oracle/", "oracle"),
    DBMS.SQLITE: (SQLITE_ALIASES, "python-sqlite", "https://docs.python.org/3/library/sqlite3.html", "sqlite"),
    DBMS.ACCESS: (ACCESS_ALIASES, "python-pyodbc", "https://github.com/mkleehammer/pyodbc", "access"),
    DBMS.FIREBIRD: (FIREBIRD_ALIASES, "python-kinterbasdb", "http://kinterbasdb.sourceforge.net/", "firebird"),
    DBMS.MAXDB: (MAXDB_ALIASES, None, None, "maxdb"),
    DBMS.SYBASE: (SYBASE_ALIASES, "python-pymssql", "https://github.com/pymssql/pymssql", "sybase"),
    DBMS.DB2: (DB2_ALIASES, "python ibm-db", "https://github.com/ibmdb/python-ibmdb", "ibm_db_sa"),
    DBMS.HSQLDB: (HSQLDB_ALIASES, "python jaydebeapi & python-jpype", "https://pypi.python.org/pypi/JayDeBeApi/ & https://github.com/jpype-project/jpype", None),
    DBMS.H2: (H2_ALIASES, None, None, None),
    DBMS.INFORMIX: (INFORMIX_ALIASES, "python ibm-db", "https://github.com/ibmdb/python-ibmdb", "ibm_db_sa"),
    DBMS.MONETDB: (MONETDB_ALIASES, "pymonetdb", "https://github.com/gijzelaerr/pymonetdb", "monetdb"),
    DBMS.DERBY: (DERBY_ALIASES, "pydrda", "https://github.com/nakagami/pydrda/", None),
    DBMS.VERTICA: (VERTICA_ALIASES, "vertica-python", "https://github.com/vertica/vertica-python", "vertica+vertica_python"),
    DBMS.MCKOI: (MCKOI_ALIASES, None, None, None),
    DBMS.PRESTO: (PRESTO_ALIASES, "presto-python-client", "https://github.com/prestodb/presto-python-client", None),
    DBMS.ALTIBASE: (ALTIBASE_ALIASES, None, None, None),
    DBMS.MIMERSQL: (MIMERSQL_ALIASES, "mimerpy", "https://github.com/mimersql/MimerPy", None),
    DBMS.CLICKHOUSE: (CLICKHOUSE_ALIASES, "clickhouse_connect", "https://github.com/ClickHouse/clickhouse-connect", None),
    DBMS.CRATEDB: (CRATEDB_ALIASES, "python-psycopg2", "https://github.com/psycopg/psycopg2", "postgresql"),
    DBMS.CUBRID: (CUBRID_ALIASES, "CUBRID-Python", "https://github.com/CUBRID/cubrid-python", None),
    DBMS.CACHE: (CACHE_ALIASES, "python jaydebeapi & python-jpype", "https://pypi.python.org/pypi/JayDeBeApi/ & https://github.com/jpype-project/jpype", None),
    DBMS.EXTREMEDB: (EXTREMEDB_ALIASES, None, None, None),
    DBMS.FRONTBASE: (FRONTBASE_ALIASES, None, None, None),
    DBMS.RAIMA: (RAIMA_ALIASES, None, None, None),
    DBMS.VIRTUOSO: (VIRTUOSO_ALIASES, None, None, None),
}

# Reference: https://blog.jooq.org/tag/sysibm-sysdummy1/
FROM_DUMMY_TABLE = {
    DBMS.ORACLE: " FROM DUAL",
    DBMS.ACCESS: " FROM MSysAccessObjects",
    DBMS.FIREBIRD: " FROM RDB$DATABASE",
    DBMS.MAXDB: " FROM VERSIONS",
    DBMS.DB2: " FROM SYSIBM.SYSDUMMY1",
    DBMS.HSQLDB: " FROM INFORMATION_SCHEMA.SYSTEM_USERS",
    DBMS.INFORMIX: " FROM SYSMASTER:SYSDUAL",
    DBMS.DERBY: " FROM SYSIBM.SYSDUMMY1",
    DBMS.MIMERSQL: " FROM SYSTEM.ONEROW",
    DBMS.FRONTBASE: " FROM INFORMATION_SCHEMA.IO_STATISTICS"
}

HEURISTIC_NULL_EVAL = {
    DBMS.ACCESS: "CVAR(NULL)",
    DBMS.MAXDB: "ALPHA(NULL)",
    DBMS.MSSQL: "DIFFERENCE(NULL,NULL)",
    DBMS.MYSQL: "QUARTER(NULL XOR NULL)",
    DBMS.ORACLE: "INSTR2(NULL,NULL)",
    DBMS.PGSQL: "QUOTE_IDENT(NULL)",
    DBMS.SQLITE: "UNLIKELY(NULL)",
    DBMS.H2: "STRINGTOUTF8(NULL)",
    DBMS.MONETDB: "CODE(NULL)",
    DBMS.DERBY: "NULLIF(USER,SESSION_USER)",
    DBMS.VERTICA: "BITSTRING_TO_BINARY(NULL)",
    DBMS.MCKOI: "TONUMBER(NULL)",
    DBMS.PRESTO: "FROM_HEX(NULL)",
    DBMS.ALTIBASE: "TDESENCRYPT(NULL,NULL)",
    DBMS.MIMERSQL: "ASCII_CHAR(256)",
    DBMS.CRATEDB: "MD5(NULL~NULL)",  # Note: NULL~NULL also being evaluated on H2 and Ignite
    DBMS.CUBRID: "(NULL SETEQ NULL)",
    DBMS.CACHE: "%SQLUPPER NULL",
    DBMS.EXTREMEDB: "NULLIFZERO(hashcode(NULL))",
    DBMS.RAIMA: "IF(ROWNUMBER()>0,CONVERT(NULL,TINYINT),NULL))",
    DBMS.VIRTUOSO: "__MAX_NOTNULL(NULL)",
    DBMS.CLICKHOUSE: "halfMD5(NULL) IS NULL",
}

SQL_STATEMENTS = {
    "SQL SELECT statement": (
        "select ",
        "show ",
        " top ",
        " distinct ",
        " from ",
        " from dual",
        " where ",
        " group by ",
        " order by ",
        " having ",
        " limit ",
        " offset ",
        " union all ",
        " rownum as ",
        "(case ",
    ),

    "SQL data definition": (
        "create ",
        "declare ",
        "drop ",
        "truncate ",
        "alter ",
    ),

    "SQL data manipulation": (
        "bulk ",
        "insert ",
        "update ",
        "delete ",
        "merge ",
        "load ",
    ),

    "SQL data control": (
        "grant ",
        "revoke ",
    ),

    "SQL data execution": (
        "exec ",
        "execute ",
        "values ",
        "call ",
    ),

    "SQL transaction": (
        "start transaction ",
        "begin work ",
        "begin transaction ",
        "commit ",
        "rollback ",
    ),

    "SQL administration": (
        "set ",
    ),
}

POST_HINT_CONTENT_TYPES = {
    PostHint.JSON: "application/json",
    PostHint.JSON_LIKE: "application/json",
    PostHint.MULTIPART: "multipart/form-data",
    PostHint.SOAP: "application/soap+xml",
    PostHint.XML: "application/xml",
    PostHint.ARRAY_LIKE: "application/x-www-form-urlencoded; charset=utf-8",
}

OBSOLETE_OPTIONS = {
    "--replicate": "use '--dump-format=SQLITE' instead",
    "--no-unescape": "use '--no-escape' instead",
    "--binary": "use '--binary-fields' instead",
    "--auth-private": "use '--auth-file' instead",
    "--ignore-401": "use '--ignore-code' instead",
    "--second-order": "use '--second-url' instead",
    "--purge-output": "use '--purge' instead",
    "--sqlmap-shell": "use '--shell' instead",
    "--check-payload": None,
    "--check-waf": None,
    "--pickled-options": "use '--api -c ...' instead",
    "--identify-waf": "functionality being done automatically",
}

DEPRECATED_OPTIONS = {
}

DUMP_DATA_PREPROCESS = {
    DBMS.ORACLE: {"XMLTYPE": "(%s).getStringVal()"},  # Reference: https://www.tibcommunity.com/docs/DOC-3643
    DBMS.MSSQL: {"IMAGE": "CONVERT(VARBINARY(MAX),%s)"},
}

DEFAULT_DOC_ROOTS = {
    OS.WINDOWS: ("C:/xampp/htdocs/", "C:/wamp/www/", "C:/Inetpub/wwwroot/"),
    OS.LINUX: ("/var/www/", "/var/www/html", "/var/www/htdocs", "/usr/local/apache2/htdocs", "/usr/local/www/data", "/var/apache2/htdocs", "/var/www/nginx-default", "/srv/www/htdocs", "/usr/local/var/www")  # Reference: https://wiki.apache.org/httpd/DistrosDefaultLayout
}

PART_RUN_CONTENT_TYPES = {
    "checkDbms": CONTENT_TYPE.TECHNIQUES,
    "getFingerprint": CONTENT_TYPE.DBMS_FINGERPRINT,
    "getBanner": CONTENT_TYPE.BANNER,
    "getCurrentUser": CONTENT_TYPE.CURRENT_USER,
    "getCurrentDb": CONTENT_TYPE.CURRENT_DB,
    "getHostname": CONTENT_TYPE.HOSTNAME,
    "isDba": CONTENT_TYPE.IS_DBA,
    "getUsers": CONTENT_TYPE.USERS,
    "getPasswordHashes": CONTENT_TYPE.PASSWORDS,
    "getPrivileges": CONTENT_TYPE.PRIVILEGES,
    "getRoles": CONTENT_TYPE.ROLES,
    "getDbs": CONTENT_TYPE.DBS,
    "getTables": CONTENT_TYPE.TABLES,
    "getColumns": CONTENT_TYPE.COLUMNS,
    "getSchema": CONTENT_TYPE.SCHEMA,
    "getCount": CONTENT_TYPE.COUNT,
    "dumpTable": CONTENT_TYPE.DUMP_TABLE,
    "search": CONTENT_TYPE.SEARCH,
    "sqlQuery": CONTENT_TYPE.SQL_QUERY,
    "tableExists": CONTENT_TYPE.COMMON_TABLES,
    "columnExists": CONTENT_TYPE.COMMON_COLUMNS,
    "readFile": CONTENT_TYPE.FILE_READ,
    "writeFile": CONTENT_TYPE.FILE_WRITE,
    "osCmd": CONTENT_TYPE.OS_CMD,
    "regRead": CONTENT_TYPE.REG_READ
}

# Reference: http://www.w3.org/TR/1999/REC-html401-19991224/sgml/entities.html

HTML_ENTITIES = {
    "quot": 34,
    "amp": 38,
    "apos": 39,
    "lt": 60,
    "gt": 62,
    "nbsp": 160,
    "iexcl": 161,
    "cent": 162,
    "pound": 163,
    "curren": 164,
    "yen": 165,
    "brvbar": 166,
    "sect": 167,
    "uml": 168,
    "copy": 169,
    "ordf": 170,
    "laquo": 171,
    "not": 172,
    "shy": 173,
    "reg": 174,
    "macr": 175,
    "deg": 176,
    "plusmn": 177,
    "sup2": 178,
    "sup3": 179,
    "acute": 180,
    "micro": 181,
    "para": 182,
    "middot": 183,
    "cedil": 184,
    "sup1": 185,
    "ordm": 186,
    "raquo": 187,
    "frac14": 188,
    "frac12": 189,
    "frac34": 190,
    "iquest": 191,
    "Agrave": 192,
    "Aacute": 193,
    "Acirc": 194,
    "Atilde": 195,
    "Auml": 196,
    "Aring": 197,
    "AElig": 198,
    "Ccedil": 199,
    "Egrave": 200,
    "Eacute": 201,
    "Ecirc": 202,
    "Euml": 203,
    "Igrave": 204,
    "Iacute": 205,
    "Icirc": 206,
    "Iuml": 207,
    "ETH": 208,
    "Ntilde": 209,
    "Ograve": 210,
    "Oacute": 211,
    "Ocirc": 212,
    "Otilde": 213,
    "Ouml": 214,
    "times": 215,
    "Oslash": 216,
    "Ugrave": 217,
    "Uacute": 218,
    "Ucirc": 219,
    "Uuml": 220,
    "Yacute": 221,
    "THORN": 222,
    "szlig": 223,
    "agrave": 224,
    "aacute": 225,
    "acirc": 226,
    "atilde": 227,
    "auml": 228,
    "aring": 229,
    "aelig": 230,
    "ccedil": 231,
    "egrave": 232,
    "eacute": 233,
    "ecirc": 234,
    "euml": 235,
    "igrave": 236,
    "iacute": 237,
    "icirc": 238,
    "iuml": 239,
    "eth": 240,
    "ntilde": 241,
    "ograve": 242,
    "oacute": 243,
    "ocirc": 244,
    "otilde": 245,
    "ouml": 246,
    "divide": 247,
    "oslash": 248,
    "ugrave": 249,
    "uacute": 250,
    "ucirc": 251,
    "uuml": 252,
    "yacute": 253,
    "thorn": 254,
    "yuml": 255,
    "OElig": 338,
    "oelig": 339,
    "Scaron": 352,
    "fnof": 402,
    "scaron": 353,
    "Yuml": 376,
    "circ": 710,
    "tilde": 732,
    "Alpha": 913,
    "Beta": 914,
    "Gamma": 915,
    "Delta": 916,
    "Epsilon": 917,
    "Zeta": 918,
    "Eta": 919,
    "Theta": 920,
    "Iota": 921,
    "Kappa": 922,
    "Lambda": 923,
    "Mu": 924,
    "Nu": 925,
    "Xi": 926,
    "Omicron": 927,
    "Pi": 928,
    "Rho": 929,
    "Sigma": 931,
    "Tau": 932,
    "Upsilon": 933,
    "Phi": 934,
    "Chi": 935,
    "Psi": 936,
    "Omega": 937,
    "alpha": 945,
    "beta": 946,
    "gamma": 947,
    "delta": 948,
    "epsilon": 949,
    "zeta": 950,
    "eta": 951,
    "theta": 952,
    "iota": 953,
    "kappa": 954,
    "lambda": 955,
    "mu": 956,
    "nu": 957,
    "xi": 958,
    "omicron": 959,
    "pi": 960,
    "rho": 961,
    "sigmaf": 962,
    "sigma": 963,
    "tau": 964,
    "upsilon": 965,
    "phi": 966,
    "chi": 967,
    "psi": 968,
    "omega": 969,
    "thetasym": 977,
    "upsih": 978,
    "piv": 982,
    "bull": 8226,
    "hellip": 8230,
    "prime": 8242,
    "Prime": 8243,
    "oline": 8254,
    "frasl": 8260,
    "ensp": 8194,
    "emsp": 8195,
    "thinsp": 8201,
    "zwnj": 8204,
    "zwj": 8205,
    "lrm": 8206,
    "rlm": 8207,
    "ndash": 8211,
    "mdash": 8212,
    "lsquo": 8216,
    "rsquo": 8217,
    "sbquo": 8218,
    "ldquo": 8220,
    "rdquo": 8221,
    "bdquo": 8222,
    "dagger": 8224,
    "Dagger": 8225,
    "permil": 8240,
    "lsaquo": 8249,
    "rsaquo": 8250,
    "euro": 8364,
    "weierp": 8472,
    "image": 8465,
    "real": 8476,
    "trade": 8482,
    "alefsym": 8501,
    "larr": 8592,
    "uarr": 8593,
    "rarr": 8594,
    "darr": 8595,
    "harr": 8596,
    "crarr": 8629,
    "lArr": 8656,
    "uArr": 8657,
    "rArr": 8658,
    "dArr": 8659,
    "hArr": 8660,
    "forall": 8704,
    "part": 8706,
    "exist": 8707,
    "empty": 8709,
    "nabla": 8711,
    "isin": 8712,
    "notin": 8713,
    "ni": 8715,
    "prod": 8719,
    "sum": 8721,
    "minus": 8722,
    "lowast": 8727,
    "radic": 8730,
    "prop": 8733,
    "infin": 8734,
    "ang": 8736,
    "and": 8743,
    "or": 8744,
    "cap": 8745,
    "cup": 8746,
    "int": 8747,
    "there4": 8756,
    "sim": 8764,
    "cong": 8773,
    "asymp": 8776,
    "ne": 8800,
    "equiv": 8801,
    "le": 8804,
    "ge": 8805,
    "sub": 8834,
    "sup": 8835,
    "nsub": 8836,
    "sube": 8838,
    "supe": 8839,
    "oplus": 8853,
    "otimes": 8855,
    "perp": 8869,
    "sdot": 8901,
    "lceil": 8968,
    "rceil": 8969,
    "lfloor": 8970,
    "rfloor": 8971,
    "lang": 9001,
    "rang": 9002,
    "loz": 9674,
    "spades": 9824,
    "clubs": 9827,
    "hearts": 9829,
    "diams": 9830
}












# Leaving (dirty) possibility to change values from here (e.g. `export ANKABUT__MAX_NUMBER_OF_THREADS=20`)

for KV, VK in os.environ.items():
    if KV.upper().startswith("%s_" % ANKABUT_ENVIRONMENT_PREFIX):
        _ = KV[len(ANKABUT_ENVIRONMENT_PREFIX) + 1:].upper()
        if _ in globals():
            Original = globals()[_]
            if isinstance(Original, int):
                try:
                    globals()[_] = int(VK)
                except ValueError:
                    pass
            elif isinstance(Original, bool):
                globals()[_] = VK.lower() in ('1', 'true')
            elif isinstance(Original, (list, tuple)):
                globals()[_] = [__.strip() for __ in _.split(',')]
            else:
                globals()[_] = VK


























































































