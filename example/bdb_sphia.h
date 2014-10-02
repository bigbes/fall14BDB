#include "third_party/sophia/db/sophia.h"

struct DBT {
	void  *data;
	size_t size;
};

struct DB {
	/* Public API */
	int (*close)(struct DB *db);
	int (*del)(const struct DB *db, const struct DBT *key);
	int (*get)(const struct DB *db, const struct DBT *key,
			struct DBT *data);
	int (*put)(const struct DB *db, const struct DBT *key,
			const struct DBT *data);

	/* Private API */
	void *env;
	void *db;
};

struct DBC {
	size_t db_size;
	size_t chunk_size;
};

struct DB *dbcreate(const char *path, const struct DBC conf);
struct DB *dbopen  (const char *path, const struct DBC conf);

int db_close(struct DB *db);
int db_del(const struct DB *, void *, size_t);
int db_get(const struct DB *, void *, size_t, void **, size_t *);
int db_put(const struct DB *, void *, size_t, void * , size_t  );
