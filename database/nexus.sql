BEGIN;

CREATE TABLE saved_game (
	id_saved_game INTEGER PRIMARY KEY AUTOINCREMENT,
	id_player INT REFERENCES player (id_player),
	id_character INT REFERENCES `character` (id_character),
	snapshot_player TEXT
);

INSERT INTO saved_game (id_player, id_character, snapshot_player) VALUES
	(NULL, NULL, ''), (NULL, NULL, ''), (NULL, NULL, '');

COMMIT;
