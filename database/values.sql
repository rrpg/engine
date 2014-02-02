INSERT INTO species (name_m, name_f, description) VALUES ('humain', 'humaine', 'Les humains viennent de la planete Terre');

INSERT INTO gender (name) VALUES ('male');
INSERT INTO gender (name) VALUES ('female');

INSERT INTO item (name, weight, flags, effects) VALUES ('Heavy breastplate', 5, 3, '{"defense": 10, "speed": -5}');
INSERT INTO item (name, weight, flags, effects) VALUES ('Mist potion', .1, 6, '{"stealth": 7}');

INSERT INTO region (region_name) VALUES ('Balmora');
INSERT INTO area_type (name) VALUES ('land');
INSERT INTO area_type (name) VALUES ('dungeon');
INSERT INTO area (id_region, id_area_type, container, x, y, directions, items)
	VALUES (1, (SELECT id_area_type FROM area_type WHERE name = 'land'), 'world', 0, 0, 4, '{"1": {"quantity": 1}, "2": {"quantity": 4}}');
INSERT INTO area (id_region, id_area_type, container, x, y, directions)
	VALUES (1, (SELECT id_area_type FROM area_type WHERE name = 'land'), 'world', 0, 1, 1);

INSERT INTO place (id_area, id_area_type, name) VALUES (1, (SELECT id_area_type FROM area_type WHERE name = 'dungeon'), 'first dungeon');

INSERT INTO `character` (name, id_species, id_gender, id_area) VALUES ('Tom', 1, 1, 2);
INSERT INTO talk_answer (trigger_word, sentence, condition) VALUES ('hi', "Hi, my name is Tom, I'm a butcher", '{"met":0}');
INSERT INTO talk_answer (trigger_word, sentence, condition) VALUES ('hi', 'Hi, %(player_name)s', '{"met":1}');

INSERT INTO character_answer (id_character, id_talk_answer) VALUES (1, 1);
INSERT INTO character_answer (id_character, id_talk_answer) VALUES (1, 2);
