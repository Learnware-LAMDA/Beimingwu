
ALTER TABLE tb_user_learnware_relation
ADD COLUMN verify_status VARCHAR(10) DEFAULT 'WAITING' NOT NULL,
ADD COLUMN verify_log TEXT;

CREATE INDEX idx_user_learnware_relation_verify_status ON tb_user_learnware_relation (verify_status);

UPDATE tb_user_learnware_relation SET verify_status = 'SUCCESS', verify_log = '';

CREATE TABLE tb_global_counter(
    name TEXT PRIMARY KEY,
    value INTEGER NOT NULL DEFAULT 0
);

INSERT INTO tb_global_counter (name, value) VALUES ('learnware_id', 30);

COMMIT;