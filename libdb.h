#include <string.h>

/* check `man dbopen` */
struct DBT {
     void  *data;
     size_t size;
};

struct DB{
    /* Public API */
    int (*close)(const struct DB *db);
    int (*del)(const struct DB *db, const struct DBT *key);
    int (*get)(const struct DB *db, struct DBT *key, struct DBT *data);
    int (*put)(const struct DB *db, struct DBT *key, const struct DBT *data);
    int (*sync)(const struct DB *db);
    /* Private API */
    /* ... */
}; /* Need for supporting multiple backends (HASH/BTREE) */

struct DBC {
        /* Maximum on-disk file size */
        /* 512MB by default */
        size_t db_size;
        /* Maximum chunk (node/data chunk) size */
        /* 4KB by default */
        size_t chunk_size;
        /* Maximum memory size */
        /* 16MB by default */
        size_t mem_size;
};

struct DB *dbcreate(const char *file, const struct DBC conf);
struct DB *dbopen  (const char *file); /* Metadata in file */
