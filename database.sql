CREATE TABLE "aggregates" (
    uuid VARCHAR(36) NOT NULL PRIMARY KEY,
    version int NOT NULL DEFAULT 1
);

CREATE TABLE "events" (
    uuid VARCHAR(36) NOT NULL PRIMARY KEY,
    aggregate_uuid VARCHAR(36) NOT NULL REFERENCES "aggregates" ("uuid"),
    name VARCHAR(50) NOT NULL,
    data json
);

CREATE INDEX aggregate_uuid_idx ON "events" ("aggregate_uuid");