INSERT INTO species (name_m, name_f, description) VALUES ('humain', 'humaine', 'Les humains viennent de la planete Terre');

INSERT INTO gender (name) VALUES ('male');
INSERT INTO gender (name) VALUES ('female');

INSERT INTO item (name, weight, flags, effects) VALUES ('Heavy breastplate', 5, 3, '{"defense": 10, "speed": -5}');
INSERT INTO item (name, weight, flags, effects) VALUES ('Mist potion', .1, 6, '{"stealth": 7}');

INSERT INTO region (region_name) VALUES ('Balmora');
INSERT INTO area (id_region, items) VALUES (1, '[1,2]'); -- ID 1
INSERT INTO area (id_region) VALUES (1); -- ID 2
UPDATE area SET id_next_area_east = 2 WHERE id_area = 1;
UPDATE area SET id_next_area_west = 1 WHERE id_area = 2;

INSERT INTO `character` (name, id_species, id_gender, id_area) VALUES ('Tom', 1, 1, 2);
INSERT INTO talk_answer (trigger_word, sentence, condition) VALUES ('hi', "Hi, my name is Tom, I'm a butcher", '{"met":0}');
INSERT INTO talk_answer (trigger_word, sentence, condition) VALUES ('hi', 'Hi, %(player_name)s', '{"met":1}');

INSERT INTO character_answer (id_character, id_talk_answer) VALUES (1, 1);
INSERT INTO character_answer (id_character, id_talk_answer) VALUES (1, 2);
