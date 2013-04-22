CREATE TABLE species (
    id_species INTEGER PRIMARY KEY AUTOINCREMENT,
    name_m VARCHAR(30) NOT NULL,
    name_f VARCHAR(30) NOT NULL,
    description TEXT
);

CREATE TABLE gender (
    id_gender INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(30) NOT NULL
);

CREATE TABLE `character` (
    id_character INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(30) NOT NULL,
    inventory TEXT,
    id_species INT REFERENCES species (id_species),
    id_gender INT REFERENCES gender (id_gender),
    id_area INT REFERENCES area (id_area)
);

CREATE INDEX character_id_area ON character (id_area);

CREATE TABLE player (
    id_player INTEGER PRIMARY KEY AUTOINCREMENT,
    login VARCHAR(30) NOT NULL,
    password VARCHAR(40) NOT NULL,
    id_character INT REFERENCES `character` (id_character)
);

CREATE TABLE met (
    id_player INT REFERENCES player (id_player),
    id_character INT REFERENCES `character` (id_character)
);

-- talk module

CREATE TABLE talk_answer (
    id_talk_answer INTEGER PRIMARY KEY AUTOINCREMENT,
    trigger_word VARCHAR(128) NOT NULL,
    sentence TEXT NOT NULL,
    condition TEXT
);

CREATE TABLE character_answer (
    id_character INT REFERENCES `character` (id_character),
    id_talk_answer INT REFERENCES talk_answer (id_talk_answer)
);

-- moves module

CREATE TABLE region (
    id_region INTEGER PRIMARY KEY AUTOINCREMENT,
    region_name VARCHAR(30) NOT NULL,
    can_sleep_in BOOLEAN DEFAULT TRUE
);

CREATE TABLE area (
    id_area INTEGER PRIMARY KEY AUTOINCREMENT,
    id_region INTEGER REFERENCES region (id_region),
    id_next_area_north INTEGER REFERENCES area (id_area),
    id_next_area_east INTEGER REFERENCES area (id_area),
    id_next_area_south INTEGER REFERENCES area (id_area),
    id_next_area_west INTEGER REFERENCES area (id_area),
    items TEXT
);

CREATE TABLE item (
	id_item INTEGER PRIMARY KEY AUTOINCREMENT,
	name VARCHAR(50) NOT NULL,
	weight FLOAT NOT NULL DEFAULT 0.0,
	flags LONG INTEGER NOT NULL DEFAULT 0,
	effects TEXT
);
