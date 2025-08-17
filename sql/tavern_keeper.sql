-- Normalized Chatbot Schema (MySQL 8.0+)
-- Includes: functions, intents, patterns, responses, arguments, argument_values
-- Seeds with Tavern Keeper NPC intents and 'end_conversation' function.

-- Safety options
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- Create database
CREATE DATABASE IF NOT EXISTS chatbot
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE chatbot;

-- Drop existing tables in reverse dependency order
DROP TABLE IF EXISTS argument_values;
DROP TABLE IF EXISTS arguments;
DROP TABLE IF EXISTS responses;
DROP TABLE IF EXISTS patterns;
DROP TABLE IF EXISTS intents;
DROP TABLE IF EXISTS functions;

SET FOREIGN_KEY_CHECKS = 1;

-- =======================
-- Core Tables
-- =======================

-- Functions: e.g., 'end_conversation'
CREATE TABLE functions (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(150) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT uq_functions_name UNIQUE (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Intents: nullable function_id
CREATE TABLE intents (
  id INT AUTO_INCREMENT PRIMARY KEY,
  tag VARCHAR(150) NOT NULL,
  function_id INT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT uq_intents_tag UNIQUE (tag),
  CONSTRAINT fk_intents_function
    FOREIGN KEY (function_id) REFERENCES functions(id)
    ON UPDATE CASCADE
    ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE INDEX idx_intents_function_id ON intents(function_id);

-- Patterns: N:1 to intents
CREATE TABLE patterns (
  id INT AUTO_INCREMENT PRIMARY KEY,
  pattern VARCHAR(255) NOT NULL,
  intent_id INT NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_patterns_intent
    FOREIGN KEY (intent_id) REFERENCES intents(id)
    ON UPDATE CASCADE
    ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE INDEX idx_patterns_intent_id ON patterns(intent_id);
CREATE INDEX idx_patterns_pattern ON patterns(pattern);

-- Responses: N:1 to intents
CREATE TABLE responses (
  id INT AUTO_INCREMENT PRIMARY KEY,
  response TEXT NOT NULL,
  intent_id INT NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_responses_intent
    FOREIGN KEY (intent_id) REFERENCES intents(id)
    ON UPDATE CASCADE
    ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE INDEX idx_responses_intent_id ON responses(intent_id);

-- Arguments: function-level formal parameters
CREATE TABLE arguments (
  id INT AUTO_INCREMENT PRIMARY KEY,
  argument_name VARCHAR(150) NOT NULL,
  function_id INT NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_arguments_function
    FOREIGN KEY (function_id) REFERENCES functions(id)
    ON UPDATE CASCADE
    ON DELETE CASCADE,
  CONSTRAINT uq_arguments_function_name UNIQUE (function_id, argument_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE INDEX idx_arguments_function_id ON arguments(function_id);

-- Argument Values: values bound to a specific argument
CREATE TABLE argument_values (
  id INT AUTO_INCREMENT PRIMARY KEY,
  value VARCHAR(255) NOT NULL,
  argument_id INT NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_argument_values_argument
    FOREIGN KEY (argument_id) REFERENCES arguments(id)
    ON UPDATE CASCADE
    ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE INDEX idx_argument_values_argument_id ON argument_values(argument_id);
CREATE INDEX idx_argument_values_value ON argument_values(value);

-- =======================
-- Seed Data
-- =======================

-- Functions
INSERT INTO functions (name) VALUES ('end_conversation');

-- Intents (with function link for 'farewell')
INSERT INTO intents (tag, function_id) VALUES
  ('greeting', NULL),
  ('ask_drink', NULL),
  ('ask_food', NULL),
  ('ask_gossip', NULL),
  ('farewell', (SELECT id FROM functions WHERE name='end_conversation'));

-- Patterns
-- greeting
INSERT INTO patterns (pattern, intent_id)
  SELECT 'Hello', id FROM intents WHERE tag='greeting';
INSERT INTO patterns (pattern, intent_id)
  SELECT 'Hi there', id FROM intents WHERE tag='greeting';
INSERT INTO patterns (pattern, intent_id)
  SELECT 'Greetings', id FROM intents WHERE tag='greeting';
INSERT INTO patterns (pattern, intent_id)
  SELECT 'Good evening', id FROM intents WHERE tag='greeting';
INSERT INTO patterns (pattern, intent_id)
  SELECT 'Hey', id FROM intents WHERE tag='greeting';

-- ask_drink
INSERT INTO patterns (pattern, intent_id)
  SELECT 'What do you have to drink?', id FROM intents WHERE tag='ask_drink';
INSERT INTO patterns (pattern, intent_id)
  SELECT 'I''d like a drink', id FROM intents WHERE tag='ask_drink';
INSERT INTO patterns (pattern, intent_id)
  SELECT 'Ale please', id FROM intents WHERE tag='ask_drink';
INSERT INTO patterns (pattern, intent_id)
  SELECT 'Got any wine?', id FROM intents WHERE tag='ask_drink';
INSERT INTO patterns (pattern, intent_id)
  SELECT 'What''s on tap?', id FROM intents WHERE tag='ask_drink';
INSERT INTO patterns (pattern, intent_id)
  SELECT 'Can I get a beer?', id FROM intents WHERE tag='ask_drink';

-- ask_food
INSERT INTO patterns (pattern, intent_id)
  SELECT 'What food do you serve?', id FROM intents WHERE tag='ask_food';
INSERT INTO patterns (pattern, intent_id)
  SELECT 'I''d like some food', id FROM intents WHERE tag='ask_food';
INSERT INTO patterns (pattern, intent_id)
  SELECT 'Got any meals?', id FROM intents WHERE tag='ask_food';
INSERT INTO patterns (pattern, intent_id)
  SELECT 'What’s for dinner?', id FROM intents WHERE tag='ask_food';
INSERT INTO patterns (pattern, intent_id)
  SELECT 'I’m hungry', id FROM intents WHERE tag='ask_food';

-- ask_gossip
INSERT INTO patterns (pattern, intent_id)
  SELECT 'Heard any rumors?', id FROM intents WHERE tag='ask_gossip';
INSERT INTO patterns (pattern, intent_id)
  SELECT 'What’s the news?', id FROM intents WHERE tag='ask_gossip';
INSERT INTO patterns (pattern, intent_id)
  SELECT 'Any gossip?', id FROM intents WHERE tag='ask_gossip';
INSERT INTO patterns (pattern, intent_id)
  SELECT 'What’s happening around here?', id FROM intents WHERE tag='ask_gossip';
INSERT INTO patterns (pattern, intent_id)
  SELECT 'Tell me a story', id FROM intents WHERE tag='ask_gossip';

-- farewell
INSERT INTO patterns (pattern, intent_id)
  SELECT 'Goodbye', id FROM intents WHERE tag='farewell';
INSERT INTO patterns (pattern, intent_id)
  SELECT 'Farewell', id FROM intents WHERE tag='farewell';
INSERT INTO patterns (pattern, intent_id)
  SELECT 'I must be going', id FROM intents WHERE tag='farewell';
INSERT INTO patterns (pattern, intent_id)
  SELECT 'See you later', id FROM intents WHERE tag='farewell';
INSERT INTO patterns (pattern, intent_id)
  SELECT 'Thanks for the hospitality', id FROM intents WHERE tag='farewell';

-- Responses
-- greeting
INSERT INTO responses (response, intent_id)
  SELECT 'Well met, traveler! Welcome to the Drunken Dragon Inn.', id FROM intents WHERE tag='greeting';
INSERT INTO responses (response, intent_id)
  SELECT 'Ah, a new face! Pull up a chair and rest your weary feet.', id FROM intents WHERE tag='greeting';
INSERT INTO responses (response, intent_id)
  SELECT 'Greetings, adventurer. What brings you to my humble tavern?', id FROM intents WHERE tag='greeting';

-- ask_drink
INSERT INTO responses (response, intent_id)
  SELECT 'We''ve got the finest dwarven ale, elven wine, and a mysterious brew I wouldn’t recommend after midnight.', id FROM intents WHERE tag='ask_drink';
INSERT INTO responses (response, intent_id)
  SELECT 'A pint of dwarven stout or a glass of elven mead, the choice is yours!', id FROM intents WHERE tag='ask_drink';
INSERT INTO responses (response, intent_id)
  SELECT 'For the brave, I’ve got a flaming dragon whiskey — care to try?', id FROM intents WHERE tag='ask_drink';

-- ask_food
INSERT INTO responses (response, intent_id)
  SELECT 'We’ve roasted boar, stew thick enough to stand a spoon in, and bread fresh from the ovens.', id FROM intents WHERE tag='ask_food';
INSERT INTO responses (response, intent_id)
  SELECT 'You’ll find no finer mutton stew this side of the mountains.', id FROM intents WHERE tag='ask_food';
INSERT INTO responses (response, intent_id)
  SELECT 'Hungry, eh? A platter of cheese and bread will keep you strong for your travels.', id FROM intents WHERE tag='ask_food';

-- ask_gossip
INSERT INTO responses (response, intent_id)
  SELECT 'They say a dragon was spotted near the old ruins to the north… though I don’t fancy seeing it myself.', id FROM intents WHERE tag='ask_gossip';
INSERT INTO responses (response, intent_id)
  SELECT 'Rumor has it the king’s treasury has gone missing — and the thieves are hiding in plain sight.', id FROM intents WHERE tag='ask_gossip';
INSERT INTO responses (response, intent_id)
  SELECT 'Some say the forest spirits are restless again. Might be trouble for travelers.', id FROM intents WHERE tag='ask_gossip';

-- farewell
INSERT INTO responses (response, intent_id)
  SELECT 'Safe travels, adventurer. May fortune favor you.', id FROM intents WHERE tag='farewell';
INSERT INTO responses (response, intent_id)
  SELECT 'Until next time, traveler. The fire will be waiting for your return.', id FROM intents WHERE tag='farewell';
INSERT INTO responses (response, intent_id)
  SELECT 'Go with the gods, and may your mug never run dry.', id FROM intents WHERE tag='farewell';
