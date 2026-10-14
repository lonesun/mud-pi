BEGIN TRANSACTION;

CREATE TABLE roster (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    current_room TEXT,
    description TEXT
);

INSERT INTO roster (name, current_room, description) VALUES('mauvalong', 'Forest', 'A mysterious wanderer');

COMMIT;