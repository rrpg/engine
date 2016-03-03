BEGIN;
INSERT INTO species (name, description) VALUES ('Human', 'Humans come from planet Earth');

INSERT INTO gender (name) VALUES ('male');
INSERT INTO gender (name) VALUES ('female');

INSERT INTO item (name, weight, flags, effects) VALUES ('Heavy breastplate', 5, 3, '{"defense": 10, "speed": -5}');
INSERT INTO item (name, weight, flags, effects) VALUES ('Mist potion', .1, 6, '{"stealth": 7}');

INSERT INTO region (region_name) VALUES ('The High lands');
INSERT INTO area_type (name) VALUES ('hostile');
INSERT INTO area_type (name) VALUES ('peaceful');
INSERT INTO area_type (name) VALUES ('dungeon');

-- Map of the test world
--	+-+
--	| |
--	+-+
--	+---------+
--	|         |
--	|         |
--	|2, (0, 1)|
--	|         |
--	|         |
--	+---| |---+
--	+---| |---++---------+
--	|         ||         |
--	|         ||         |
--	|1, (0, 0)==3, (1, 0)|
--	|         ||         |
--	|         ||         |
--	+---------++---------+
--
--
--
--
--
--
--
--
--
INSERT INTO area (id_region, id_area_type, container, x, y, directions, items)
	VALUES (1, (SELECT id_area_type FROM area_type WHERE name = 'peaceful'), 'world', 0, 0, 3, '{"1": {"quantity": 1}, "2": {"quantity": 4}}');
INSERT INTO area (id_region, id_area_type, container, x, y, directions, items)
	VALUES (1, (SELECT id_area_type FROM area_type WHERE name = 'peaceful'), 'world', 0, 1, 4, '{"1": {"quantity": 6}}');
INSERT INTO area (id_region, id_area_type, container, x, y, directions)
	VALUES (1, (SELECT id_area_type FROM area_type WHERE name = 'hostile'), 'world', 1, 0, 8);

INSERT INTO item_container_type (label) VALUES ('chest');
INSERT INTO item_container_type (label) VALUES ('box');
INSERT INTO item_container_type (label) VALUES ('wardrobe');
INSERT INTO item_container (id_item_container_type, id_area, items) VALUES (1, 2, '{"1": {"quantity": 4}}');
INSERT INTO item_container (id_item_container_type, id_area, items) VALUES (3, 2, '{"1": {"quantity": 4}}');
INSERT INTO item_container (id_item_container_type, id_area, items) VALUES (3, 2, '{"2": {"quantity": 4}}');

INSERT INTO settings (key, value) VALUES ('START_CELL_ID', 1);

INSERT INTO place (id_area, id_area_type, name) VALUES (2, (SELECT id_area_type FROM area_type WHERE name = 'dungeon'), 'first dungeon');

INSERT INTO `character` (name, id_species, id_gender, id_area) VALUES ('Tom', 1, 1, 2);
INSERT INTO talk_answer (trigger_word, sentence, condition) VALUES ('hi', "Hi, my name is Tom, I'm a butcher", '{"met":0}');
INSERT INTO talk_answer (trigger_word, sentence, condition) VALUES ('hi', 'Hi, %(player_name)s', '{"met":1}');

INSERT INTO character_answer (id_character, id_talk_answer) VALUES (1, 1);
INSERT INTO character_answer (id_character, id_talk_answer) VALUES (1, 2);

INSERT INTO creature (name, stat_hp, stat_strength, stat_defence, stat_speed, stat_accuracy)
	VALUES ("rat", 15, 2, 2, 2, 75);

INSERT INTO creature_area_type (id_creature, id_area_type, probability)
	VALUES (1, 1, 1.0); -- rat in hostile area

-- For UT
INSERT INTO `character` (name, id_species, id_gender, id_area) VALUES ('TEST_PLAYER', 1, 1, 2);
INSERT INTO player (id_character, login) VALUES (2, 'TEST_PLAYER');


COMMIT;
