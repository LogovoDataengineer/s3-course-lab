#!/bin/sh
# Выполняется контейнером init при каждом `make up`. Повторный запуск ничего не ломает.
# Создаёт двух учебных пользователей MinIO и выдаёт им права из папки policies/:
#   course-writer — читает и пишет объекты в бакете course-lake;
#   course-reader — только читает префикс curated/ бакета course-lake.
# Сам бакет course-lake не создаётся: его создаёте вы в уроке L02.
set -eu
mc() { command mc --config-dir /tmp/mc "$@"; }
mc alias set course http://minio:9000 "$MINIO_ROOT_USER" "$MINIO_ROOT_PASSWORD" >/dev/null
mc admin policy create course course-writer /policies/writer.json >/dev/null
mc admin policy create course course-reader /policies/reader.json >/dev/null
mc admin user add course course-writer local-writer-123456 >/dev/null
mc admin user add course course-reader local-reader-123456 >/dev/null
mc admin policy attach course course-writer --user course-writer >/dev/null 2>&1 || true
mc admin policy attach course course-reader --user course-reader >/dev/null 2>&1 || true
echo "Пользователи course-writer и course-reader готовы."
