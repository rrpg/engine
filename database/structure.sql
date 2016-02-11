BEGIN;

CREATE TABLE species (
	id_species INTEGER PRIMARY KEY AUTOINCREMENT,
	name VARCHAR(30) NOT NULL,
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
	can_fight BIT NOT NULL DEFAULT 1,
	is_fighting BIT NOT NULL DEFAULT 0,
	stat_current_hp TINYINT NOT NULL DEFAULT 10,
	stat_max_hp TINYINT NOT NULL DEFAULT 10,
	stat_strength TINYINT NOT NULL DEFAULT 1,
	stat_defence TINYINT NOT NULL DEFAULT 1,
	stat_speed TINYINT NOT NULL DEFAULT 1,
	stat_accuracy TINYINT NOT NULL DEFAULT 1,
	id_species INT REFERENCES species (id_species),
	id_gender INT REFERENCES gender (id_gender),
	id_area INT REFERENCES area (id_area)
);

CREATE INDEX character_id_area ON character (id_area);

CREATE TABLE player (
	id_player INTEGER PRIMARY KEY AUTOINCREMENT,
	login VARCHAR(30) NOT NULL,
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

CREATE TABLE area_type (
	id_area_type INTEGER PRIMARY KEY AUTOINCREMENT,
	name VARCHAR(127) UNIQUE NOT NULL
);

CREATE TABLE area (
	id_area INTEGER PRIMARY KEY AUTOINCREMENT,
	id_area_type INTEGER REFERENCES area_type (id_area_type),
	id_region INTEGER REFERENCES region (id_region),
	container TEXT NOT NULL, -- arbitrary string used to group the areas. Each container has its own grid.
	x INTEGER NOT NULL,
	y INTEGER NOT NULL,
	directions INTEGER NOT NULL,
	items TEXT
);
CREATE UNIQUE INDEX unique_area_coordinates ON area (container, x, y);

CREATE TABLE place (
	id_place INTEGER PRIMARY KEY AUTOINCREMENT,
	id_area_type INTEGER REFERENCES area_type (id_area_type),
	id_area INTEGER REFERENCES area (id_area),
	name VARCHAR(127) NOT NULL,
	place_size INTEGER NOT NULL DEFAULT 0,
	entrance_id INTEGER REFERENCES area (id_area)
);

CREATE TABLE item_container (
	id_item_container INTEGER PRIMARY KEY AUTOINCREMENT,
	id_item_container_type INTEGER REFERENCES item_container_type (id_item_container_type),
	id_area INTEGER REFERENCES area (id_area),
	items TEXT
);
CREATE INDEX idx_item_container_id_area ON item_container (id_area);
CREATE INDEX idx_item_container_id_item_container_type ON item_container (id_item_container_type);

CREATE TABLE item_container_type (
	id_item_container_type INTEGER PRIMARY KEY AUTOINCREMENT,
	label VARCHAR(30) UNIQUE NOT NULL
);

CREATE TABLE item (
	id_item INTEGER PRIMARY KEY AUTOINCREMENT,
	name VARCHAR(50) NOT NULL,
	weight FLOAT NOT NULL DEFAULT 0.0,
	flags LONG INTEGER NOT NULL DEFAULT 0,
	effects TEXT
);

CREATE TABLE settings (
	id_setting INTEGER PRIMARY KEY AUTOINCREMENT,
	key VARCHAR(50) NOT NULL,
	value VARCHAR(50) NOT NULL
);

CREATE TABLE creature (
	id_creature INTEGER PRIMARY KEY AUTOINCREMENT,
	name VARCHAR(50),
	stat_hp TINYINT NOT NULL DEFAULT 10,
	stat_strength TINYINT NOT NULL DEFAULT 1,
	stat_defence TINYINT NOT NULL DEFAULT 1,
	stat_speed TINYINT NOT NULL DEFAULT 1,
	stat_accuracy TINYINT NOT NULL DEFAULT 1
);

CREATE TABLE creature_area_type (
	id_creature INTEGER REFERENCES creature (id_creature),
	id_area_type INTEGER REFERENCES area_type (id_area_type),
	probability FLOAT NOT NULL DEFAULT 1.0,
	PRIMARY KEY (id_creature, id_area_type)
);

CREATE TABLE creature_can_drop (
	id_creature INTEGER REFERENCES creature (id_creature),
	id_item INTEGER REFERENCES item (id_item),
	PRIMARY KEY (id_creature, id_item)
);

COMMIT;
