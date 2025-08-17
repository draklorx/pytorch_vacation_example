
/* Export Chatbot Schema as JSON (MySQL 8.0+)
   - Produces one row with a single JSON column: chatbot_json
   - Includes functions (+ arguments & values) and intents (+ function, patterns, responses)
*/

USE chatbot;

SELECT JSON_OBJECT(
  'exported_at', DATE_FORMAT(UTC_TIMESTAMP(), '%Y-%m-%dT%H:%i:%sZ'),
  'functions',
    (
      SELECT IFNULL(JSON_ARRAYAGG(
        JSON_OBJECT(
          'id', f.id,
          'name', f.name,
          'arguments',
            (
              SELECT IFNULL(JSON_ARRAYAGG(
                JSON_OBJECT(
                  'id', a.id,
                  'argument_name', a.argument_name,
                  'values',
                    (
                      SELECT IFNULL(JSON_ARRAYAGG(av.value ORDER BY av.id), JSON_ARRAY())
                      FROM argument_values av
                      WHERE av.argument_id = a.id
                    )
                )
              ORDER BY a.id), JSON_ARRAY())
              FROM arguments a
              WHERE a.function_id = f.id
            )
        )
      ORDER BY f.id), JSON_ARRAY())
      FROM functions f
    ),
  'intents',
    (
      SELECT IFNULL(JSON_ARRAYAGG(
        JSON_OBJECT(
          'id', i.id,
          'tag', i.tag,
          'function',
            (
              SELECT IF(i.function_id IS NULL, NULL,
                JSON_OBJECT('id', f.id, 'name', f.name)
              )
              FROM functions f
              WHERE f.id = i.function_id
            ),
          'patterns',
            (
              SELECT IFNULL(JSON_ARRAYAGG(p.pattern ORDER BY p.id), JSON_ARRAY())
              FROM patterns p
              WHERE p.intent_id = i.id
            ),
          'responses',
            (
              SELECT IFNULL(JSON_ARRAYAGG(r.response ORDER BY r.id), JSON_ARRAY())
              FROM responses r
              WHERE r.intent_id = i.id
            )
        )
      ORDER BY i.id), JSON_ARRAY())
      FROM intents i
    )
) AS intents_json;
