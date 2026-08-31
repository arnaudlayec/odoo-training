# `odoo.conf` reference (Odoo 19.0)

This document is based on 2 official sources only:

- [`odoo/tools/config.py`](https://github.com/odoo/odoo/blob/19.0/odoo/tools/config.py)
  (the actual option definitions, defaults and CLI help strings)
- [System configuration](https://www.odoo.com/documentation/19.0/administration/on_premise/deploy.html)
  (the deployment/production guide)

The parameter also exists:
- as a CLI flag (e.g. `db_host` ↔ `--db_host`) - for all of them
- as an environment variable (e.g. `ODOO_DB_HOST`) - for most of them - or, for
  PostgreSQL-related ones, the standard `PG*` variables libpq already uses

The precedence rule, from weaker to stronger, is:
1. hardcoded default
2. config file
3. environment variable
4. CLI flag

## General / startup

| Parameter | Default | CLI flag | Description |
|---|---|---|---|
| `addons_path` | *(empty)* | `--addons-path` | Comma-separated list of directories scanned for addons (modules). Each entry must be a folder whose immediate subfolders contain `__init__.py` + `__manifest__.py`. If empty, Odoo will only load its core module (equivalent to `./odoo/addons,./addons`) |
| `data_dir` | OS-dependent (`~/.local/share/Odoo` on Linux, or `/var/lib/odoo` without a home dir) | `-D`, `--data-dir` | Root directory where Odoo stores its own data: filestore (attachments), sessions, and the addons cache. |
| `pidfile` | *(empty)* | `--pidfile` | File where the server writes its PID. Useful for init scripts / systemd. |
| `server_wide_modules` | `base,rpc,web` | `--load` | Modules loaded once at server startup, for **every** database, regardless of whether they are "installed" on that DB (e.g. `web`, `queue_job`). `base` and `web` are always force-added even if you omit them. |
| `skip_auto_install` | `False` | `--skip-auto-install` | Skip the automatic installation of modules flagged `auto_install = True` (dependencies normally pulled in automatically, e.g. `account` pulling `sale` glue modules). Very unusual to set to `True` |
| `csv_internal_sep` | `,` | *(file only)* | Separator Odoo uses internally when it needs to encode/decode CSV-like values. Essentially never needs changing. |

## HTTP / Web

| Parameter | Default | CLI flag | Description |
|---|---|---|---|
| `http_enable` | `True` | `--no-http` (sets it to `False`) | Enables the HTTP (and longpolling/websocket) service. Disable it only on a dedicated cron-only worker (see [Cron Workers](https://www.odoo.com/documentation/19.0/administration/on_premise/deploy.html#cron-workers) when running Odoo as a WSGI app). |
| `http_interface` | `0.0.0.0` | `--http-interface` | Network interface the HTTP service binds to. `config.py` logs a warning if left unset, because the default is planned to change to `127.0.0.1` in Odoo 20.0. |
| `http_port` | `8069` | `-p`, `--http-port` | Main HTTP port (web client, website, JSON-RPC/XML-RPC API). |
| `gevent_port` | `8072` | `--gevent-port` | Port of the dedicated **gevent** worker used for the live chat / websocket traffic in multi-processing mode (`workers > 0`). |
| `proxy_mode` | `False` | `--proxy-mode` | Trust `X-Forwarded-*` headers (host, scheme, IP) sent by a reverse proxy instead of the raw connection info. **Only enable this when Odoo genuinely sits behind a trusted reverse proxy** (nginx/traefik) — otherwise a client could spoof its own IP/host/scheme by forging those headers. Mandatory for HTTPS termination and for routing `/websocket/` to the gevent worker. |
| `x_sendfile` | `False` | `--x-sendfile` | Delegates delivery of large files (attachments, assets) to the front web server via `X-Sendfile` (Apache) / `X-Accel-Redirect` (nginx), instead of having Odoo stream the bytes itself. Requires matching web-server configuration. |
| `dbfilter` | *(empty)* | `--db-filter` | Regex selecting which database(s) a hostname is allowed to see, using `%d` (first subdomain) or `%h` (full hostname) placeholders, e.g. `^%d$`. Mandatory as soon as several databases are reachable and non-logged (portal/website) traffic is involved, otherwise Odoo cannot guess which DB to use. Also a cornerstone of hardening a public instance. |
| `websocket_keep_alive_timeout` | `3600` (s) | *(file only)* | How long an idle websocket connection is kept open before being closed. |
| `websocket_rate_limit_burst` | `10` | *(file only)* | Number of websocket connections allowed in a short burst before rate-limiting kicks in. |
| `websocket_rate_limit_delay` | `0.2` (s) | *(file only)* | Minimal delay enforced between websocket connections once the burst allowance is exhausted. |

## Database (PostgreSQL)

| Parameter | Default | CLI flag | Env var | Description |
|---|---|---|---|---|
| `db_name` | *(empty = all)* | `-d`, `--database` | `PGDATABASE` | Comma-separated list of databases Odoo is allowed to install/update on (`-i`/`-u`). Also narrows what's visible when no `dbfilter` is set. |
| `db_user` | *(empty)* | `-r`, `--db_user` | `PGUSER` | PostgreSQL user. Should **not** be a Postgres superuser on a production instance. |
| `db_password` | *(empty)* | `-w`, `--db_password` | `PGPASSWORD` | PostgreSQL password. |
| `db_host` | *(empty = local socket)* | `--db_host` | `PGHOST` | PostgreSQL host. Empty means "connect via the local UNIX socket". |
| `db_port` | *(none = default 5432)* | `--db_port` | `PGPORT` | PostgreSQL port. |
| `db_sslmode` | `prefer` | `--db_sslmode` | `PGSSLMODE` | SSL mode for the Odoo↔PostgreSQL connection. One of `disable`, `allow`, `prefer`, `require`, `verify-ca`, `verify-full` (standard libpq values). |
| `db_app_name` | `odoo-{pid}` | `--db_app_name` | `PGAPPNAME` | Value reported as `application_name` in PostgreSQL (visible in `pg_stat_activity`); `{pid}` is replaced by the OS process id, handy to tell workers apart in monitoring. |
| `db_maxconn` | `64` | `--db_maxconn` | | Maximum number of physical PostgreSQL connections Odoo opens (connection pool size). |
| `db_maxconn_gevent` | *(none → falls back to `db_maxconn`)* | `--db_maxconn_gevent` | | Same, specifically for the gevent/live-chat worker, which tends to need far fewer DB connections. |
| `db_replica_host` | *(none)* | `--db_replica_host` | `PGHOST_REPLICA` | This is not a stable feature yet. Since 19.0, that behavior moved to `--dev=replica`. Host of a read-only PostgreSQL replica, used for read-mostly load balancing. Leaving it empty used to mean "open a local replica-style connection for dev/testing" up to 18.0. |
| `db_replica_port` | *(none)* | `--db_replica_port` | `PGPORT_REPLICA` | Port of the read replica. |
| `db_template` | `template0` | `--db-template` | `PGDATABASE_TEMPLATE` | PostgreSQL template used when Odoo creates a new database. |
| `pg_path` | *(empty, auto-detected)* | `--pg_path` | `PGPATH` | Path to the `pg_dump`/`pg_restore`/`psql` executables, used by the database manager for backup/restore/dump. |

## Security-sensitive settings

| Parameter | Default | CLI flag | Description |
|---|---|---|---|
| `admin_passwd` | `admin` | *(file only, not a CLI flag)* | The **master password**, checked before any database-management operation (create/drop/dump/restore, list databases). Only settable from the config file. Must be changed to a strong, randomly generated value before exposing an instance to the internet — the official doc even gives the recipe: `python3 -c 'import base64, os; print(base64.b64encode(os.urandom(24)))'`. |
| `list_db` | `True` | `--no-database-list` (sets it to `False`) | If `True`, the database selector/manager screens is reachable, but only for dev/demo purpose. This **MUST** be set to `False` in production. |
| `with_demo` | `False` | `--with-demo` / `--without-demo` | This **MUST** be set to `False` in production, first because we do not want demo data and also because demo data ships with well-known default logins/passwords... meaning admin/admin. In development or demo environment, this can be set to `all` which is very useful to test a module and understand its business logics from the UI. |

Other production-hardening points from the deploy guide:
- use unique, non-`admin` logins with strong passwords for every DB administrator;
- keep the PostgreSQL user non-superuser with the DB owned by a *different* Postgres user (so the
DB manager, even if reachable, cannot actually drop anything);
- terminate HTTPS in front of Odoo and only then turn on `proxy_mode`;
- `db_replica_host`/`dev_mode=replica` are only dev/test-only feature for now.

## Logging

| Parameter | Default | CLI flag | Description |
|---|---|---|---|
| `logfile` | *(empty = stdout)* | `--logfile` | File where server logs are written. |
| `syslog` | `False` | `--syslog` | Send logs to syslog instead of a file/stdout. Mutually exclusive with `logfile`. |
| `log_handler` | `:INFO` | `--log-handler` (repeatable) | Fine-grained logger configuration as `MODULE:LEVEL` pairs (empty module = root logger), e.g. `odoo.orm:DEBUG`. This is the modern, preferred way to tune verbosity per subsystem. `--log-web` and `--log-sql` are shortcuts that append `odoo.http:DEBUG` / `odoo.sql_db:DEBUG` to this list. |
| `log_level` | `info` | `--log-level` | Legacy, single global level, kept mostly for backward compatibility. Accepted values: `info`, `debug_rpc`, `warn`, `test`, `critical`, `runbot`, `debug_sql`, `error`, `debug`, `debug_rpc_answer`, `notset`. Prefer `log_handler` for anything beyond a quick blanket change. |
| `log_config` | *(empty)* | `--log-config` | Path to a JSON logging configuration file, in Python's [`dictConfig`](https://docs.python.org/3/library/logging.config.html#logging-config-dictschema) format, for advanced setups. |
| `log_db` | *(empty)* | `--log-db` | Name of a database where log entries are additionally stored (in `ir_logging`). Has a performance cost; used for centralized/DB-queryable logging. |
| `log_db_level` | `warning` | `--log-db-level` | Minimum level of the log entries written to `log_db`. |

### `log_handler` cheatsheet

**Examples** (config file):

```ini
# baseline + debug every SQL query
log_handler = :INFO,odoo.sql_db:DEBUG

# baseline + silence the werkzeug per-request access log noise
log_handler = :INFO,werkzeug:WARNING

# baseline + debug a single custom addon while developing it
log_handler = :INFO,odoo.addons.my_module:DEBUG
```

**Logics**
Each entry is `MODULE:LEVEL`:
- in the config file, separate by comma the values
- on the CLI, repeat `--log-handler` instead. Last entry wins.

**Levels** — must match one of these exactly (uppercase, case-sensitive:
`level = getattr(logging, level, logging.INFO)` in `netsvc.py`, so a typo or
wrong case silently falls back to `INFO` with **no error or warning**):

| Level | Verbosity |
|---|---|
| `DEBUG` | everything, including internal detail — noisy |
| `INFO` | normal operational messages (the default) |
| `WARNING` (or `WARN`) | unexpected but non-blocking situations |
| `ERROR` | a request/operation actually failed |
| `CRITICAL` | server-threatening failures only |

**Modules** — the most useful targets in practice:

| Module | What it controls |
|---|---|
| *(empty)* | root logger — the fallback for anything not overridden more specifically |
| `odoo` | every Odoo-namespaced logger at once |
| `odoo.orm` | ORM layer (recordset reads/writes, `_read_group`, computed fields...) |
| `odoo.http` | HTTP request/response handling — same as the `--log-web` shortcut |
| `odoo.http.rpc.request` / `odoo.http.rpc.response` | raw RPC payloads; very verbose and can contain sensitive data (passwords, session info) — dev only |
| `odoo.sql_db` | every SQL statement sent to PostgreSQL — same as the `--log-sql` shortcut |
| `odoo.addons.<module_name>` | logs from one specific addon's own logger, e.g. `odoo.addons.sale` |
| `werkzeug` | one access-log line per HTTP request from the underlying WSGI server |
| `odoo.tests` | test runner output |

## SMTP / outgoing e-mail

| Parameter | Default | CLI flag | Description |
|---|---|---|---|
| `email_from` | *(empty)* | `--email-from` | Address used as the "From" for system emails when nothing more specific applies. |
| `from_filter` | *(empty)* | `--from-filter` | Restricts which sender addresses this SMTP configuration is allowed to be used for — relevant when several `mail.server` records exist and Odoo has to decide which one to use for a given "from" address. |
| `smtp_server` | `localhost` | `--smtp` | SMTP server hostname. |
| `smtp_port` | `25` | `--smtp-port` | SMTP port. |
| `smtp_ssl` | `False` | `--smtp-ssl` | Encrypt the SMTP connection (STARTTLS). |
| `smtp_user` | *(empty)* | `--smtp-user` | SMTP authentication username. |
| `smtp_password` | *(empty)* | `--smtp-password` | SMTP authentication password. |
| `smtp_ssl_certificate_filename` | *(empty)* | `--smtp-ssl-certificate-filename` | Path to a client SSL certificate for SMTP authentication. |
| `smtp_ssl_private_key_filename` | *(empty)* | `--smtp-ssl-private-key-filename` | Path to the matching private key. |

## Multiprocessing & resource limits

Only relevant once `workers` is set to a non-zero value (multi-processing
mode). Most of these are POSIX-only (no effect on Windows).

| Parameter | Default | CLI flag | Description |
|---|---|---|---|
| `workers` | `0` | `--workers` | Number of worker **processes**. `0` = multi-threaded dev server (default, in dev); `> 0` switches to the production multi-processing model. See [sizing](#sizing) below. |
| `max_cron_threads` | `2` | `--max-cron-threads` | Number of concurrent threads/workers dedicated to processing cron jobs. |
| `limit_time_cpu` | `60` (s) | `--limit-time-cpu` | Max **CPU** time allowed per request. Beyond this, the worker handling that request is killed (`SIGXCPU`). |
| `limit_time_real` | `120` (s) | `--limit-time-real` | Max **wall-clock** time allowed per request — catches requests stuck waiting on I/O (slow queries, external calls) that `limit_time_cpu` wouldn't. |
| `limit_time_real_cron` | `-1` (= same as `limit_time_real`) | `--limit-time-real-cron` | Same, specifically for cron jobs. `0` disables the limit entirely (useful for long-running scheduled jobs). |
| `limit_time_worker_cron` | `0` (disabled) | `--limit-time-worker-cron` | Maximum lifetime of a cron worker/thread before it is recycled, independent of any single job's duration. |
| `limit_memory_soft` | `2147483648` (2048 MiB) | `--limit-memory-soft` | Soft virtual-memory ceiling per **HTTP** worker; once crossed, the worker finishes the current request, then gets recycled. |
| `limit_memory_soft_gevent` | *(none → falls back to `limit_memory_soft`)* | `--limit-memory-soft-gevent` | Same, for the gevent worker. |
| `limit_memory_hard` | `2684354560` (2560 MiB) | `--limit-memory-hard` | Hard virtual-memory ceiling; once crossed, any further memory allocation simply fails (the worker typically crashes/is killed). |
| `limit_memory_hard_gevent` | *(none → falls back to `limit_memory_hard`)* | `--limit-memory-hard-gevent` | Same, for the gevent worker. |
| `limit_request` | `65536` | `--limit-request` | Maximum number of requests a worker processes before being recycled (mitigates slow memory leaks). |
| `osv_memory_count_limit` | `0` (no limit) | `--osv-memory-count-limit` | Max number of records kept in memory-only (`TransientModel`) tables, e.g. wizards. |
| `transient_age_limit` | `1.0` (hours) | `--transient-age-limit` | How long `TransientModel` (wizard) records are kept in the database before garbage-collection. |

### Worker & memory sizing {#sizing}

Odoo's rules of thumb (deploy guide):
- worker count = `(#CPU × 2) + 1`
- 1 worker ≈ 6 concurrent users
- RAM per worker ≈ `0.8 × 150 MB + 0.2 × 1024 MB` ≈ 325 MB (mix of light/heavy requests)

**How to actually use this when a client gives you a user count:**

1. Convert users → HTTP workers needed (`÷6`), +1 for cron.
2. Pick the smallest standard vCPU tier (2/4/8/16 — what any host actually
   sells) whose capacity `(#CPU×2)+1` covers that many processes. **Never go
   below 2 vCPU**: with a single core, worker processes just context-switch
   instead of running in parallel, so `workers=0` (threaded mode) is
   actually better on a 1-vCPU box.
3. Configure `workers` for the *tier you bought*, not the bare theoretical
   minimum — you're already paying for those cores, so use them
   (`workers = tier's max capacity − 1 reserved for cron`). That's also your
   headroom for traffic spikes.
4. Add PostgreSQL + OS + Docker on top of Odoo's own RAM to get what to
   actually provision on the server.

| Up to N simultaneous users | vCPU to provision | `workers` | `max_cron_threads` | RAM used by Odoo | RAM to provision (server)¹ |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 24  | 2  | 4  | 1 | ~1.6 GB  | 4 GB  |
| 48  | 4  | 8  | 1 | ~2.9 GB  | 8 GB  |
| 96  | 8  | 16 | 2 | ~5.5 GB  | 16 GB |
| 192 | 16 | 32 | 2 | ~10.8 GB | 32 GB |

¹ Odoo's own RAM (workers × ~325 MB) plus a flat allowance for everything
else running on the box: Debian + Docker + PostgreSQL (shared_buffers,
connections, OS cache) — roughly +1.5 GB on the small tiers, +2.5 GB from
8 vCPU up since PostgreSQL wants more buffers for more concurrent
connections. The result is then rounded up to the RAM tier a host actually
sells next to that vCPU count — which is why these numbers land neatly on
2vCPU/4GB, 4vCPU/8GB, 8vCPU/16GB, 16vCPU/32GB: that's not a coincidence,
it's how cloud providers size their own instance families.

`max_cron_threads` above is a starting point; bump it (and budget the extra
CPU/RAM) if the database leans hard on scheduled/background jobs (e.g.
`queue_job`, heavy `mail.server` polling, nightly imports).

### About `limit_memory_soft` and `limit_memory_hard`

They are per-worker ceilings, not a total budget — so they don't scale
linearly depending on the number of `workers` or the server's `RAM`.
Odoo's own defaults (2 GB soft / 2.5 GB hard) already assume that only a
fraction of workers peak at once (the same 80/20 light/heavy split used
for the RAM column), and that assumption holds fine from **4 vCPU up**.

**For 2vCPU**: with only 4 workers, only 1 of them hitting the high 2.5GB
hard limit may trigger the Linux OOM-killer — which can take down PostgreSQL
with it instead of Odoo cleanly recycling the worker. It this scenario
the value should be lowered to 1.25 GB and 1.5 GB.

Tip: if the lowered hard limit on a 2 vCPU box is oftenly hit (large exports,
heavy PDF reports...), that's a sign to move up to the 4 vCPU/8 GB tier rather
than to raise the limit up.

```ini
limit_memory_soft = 1342177280 # 1.25GB
limit_memory_hard = 1610612736 # 1.5GB
```

## Testing

| Parameter | Default | CLI flag | Description |
|---|---|---|---|
| `screencasts` | *(empty)* | `--screencasts` | Directory where browser (JS/tour) test screencasts are saved, under `DIR/{db_name}/screencasts`. |
| `screenshots` | `<tmp>/odoo_tests` | `--screenshots` | Directory where screenshots of failed tests are saved, under `DIR/{db_name}/screenshots`. |

## Migration / upgrade

Directly relevant to the ALUVAL v16→v18→v20 migration and the OpenUpgrade
learning curve.

| Parameter | Default | CLI flag | Description |
|---|---|---|---|
| `upgrade_path` | *(empty)* | `--upgrade-path` | Extra path(s) scanned for OpenUpgrade-style migration scripts, on top of the ones bundled in addons paths. |
| `pre_upgrade_scripts` | *(empty)* | `--pre-upgrade-scripts` | Specific Python script(s) run **before** any module is loaded when `-u`/`--update` is used — for schema surgery that must happen ahead of the ORM touching the tables. |

## Misc / advanced

| Parameter | Default | CLI flag | Description |
|---|---|---|---|
| `geoip_city_db` | `/usr/share/GeoIP/GeoLite2-City.mmdb` | `--geoip-city-db` / `--geoip-db` | Path to the MaxMind GeoIP City database, used to geolocate visitors (e.g. website country/city detection). |
| `geoip_country_db` | `/usr/share/GeoIP/GeoLite2-Country.mmdb` | `--geoip-country-db` | Same, country-level database. |
| `unaccent` | `False` | `--unaccent` | Enable PostgreSQL's `unaccent` extension when creating new databases, for accent-insensitive search. |
| `reportgz` | `False` | *(file only)* | Gzip-compress generated PDF reports before storing them as attachments, trading a bit of CPU for filestore disk space. |

---

*Written for Odoo 19.0. Production was IA-assisted (Sonnet 5). Parameters and defaults may differ on 16.0/18.0 — check the matching tag of `odoo/tools/config.py` if working on an older branch.*
