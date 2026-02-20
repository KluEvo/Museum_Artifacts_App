-- ============================================
-- Sample Data for Museum Artifact Database
-- UUID Version
-- ============================================

-- Optional: enable UUID extension (safe if already enabled)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Clear tables (order matters because of FKs)
TRUNCATE TABLE artifact_loans CASCADE;
TRUNCATE TABLE condition_reports CASCADE;
TRUNCATE TABLE loans CASCADE;
TRUNCATE TABLE artifacts CASCADE;
TRUNCATE TABLE museums CASCADE;


-- ============================================
-- Museums
-- ============================================

INSERT INTO museums (museum_id, name, location, contact_email) VALUES
('9275c5b5-0d69-4c65-ac41-d377657f39e8', 'Metropolitan Museum of History', 'New York, USA', 'contact@metmuseum.org'),
('701d2a3f-42ab-4532-82cd-951bb3a6ea47', 'British Heritage Museum', 'London, UK', 'info@britishheritage.uk'),
('2479f157-0d26-4b62-a447-e05cdc2e1cb4', 'Louvre Antiquities Wing', 'Paris, France', 'collections@louvre.fr'),
('11e81e1d-82c9-4b30-8c4c-e9bf702057ba', 'Tokyo National Museum', 'Tokyo, Japan', 'admin@tnm.jp'),
('61447efc-d8aa-4040-a1bc-0f3edccd5648', 'Shanghai Museum', 'Shanghai, China', 'service@shanghaimuseum.cn');

-- ============================================
-- Artifacts
-- ============================================

-- Parent artifact (Armor Set)
INSERT INTO artifacts 
(artifact_id, name, accession_number, discovery_date, estimated_value, parent_artifact, museum_id)
VALUES
('76b05424-a679-4e6f-9788-a73a0c137297',
 'Samurai Armor Set',
 'TNM-ARM-001',
 '1856-04-12',
 850000.00,
 NULL,
 '11e81e1d-82c9-4b30-8c4c-e9bf702057ba');

-- Child artifacts (self-referencing)
INSERT INTO artifacts 
(artifact_id, name, accession_number, discovery_date, estimated_value, parent_artifact, museum_id)
VALUES
('ffb5f8e2-0677-4bc2-890f-c6f48d6893fb',
 'Samurai Helmet (Kabuto)',
 'TNM-ARM-001-H',
 '1856-04-12',
 250000.00,
 '76b05424-a679-4e6f-9788-a73a0c137297',
 '11e81e1d-82c9-4b30-8c4c-e9bf702057ba'),

('f6665a95-25d7-492d-8114-f9527de168bd',
 'Samurai Chest Plate',
 'TNM-ARM-001-C',
 '1856-04-12',
 300000.00,
 '76b05424-a679-4e6f-9788-a73a0c137297',
 '11e81e1d-82c9-4b30-8c4c-e9bf702057ba');

-- Independent artifacts
INSERT INTO artifacts 
(artifact_id, name, accession_number, discovery_date, estimated_value, parent_artifact, museum_id)
VALUES
('ac83f5d8-b4c4-449b-803a-03c5d4c7e17e',
 'Ancient Egyptian Sarcophagus',
 'MET-EGY-778',
 '1922-11-04',
 2000000.00,
 NULL,
 '9275c5b5-0d69-4c65-ac41-d377657f39e8'),

('23230050-202b-47b4-88b1-a67756706623',
 'Roman Marble Bust of Caesar',
 'BHM-ROM-102',
 '1898-06-21',
 1250000.00,
 NULL,
 '701d2a3f-42ab-4532-82cd-951bb3a6ea47'),

('391352cb-1b64-4a69-a76e-175aa923e095',
 'Medieval Illuminated Manuscript',
 'LOU-MED-334',
 '1875-03-15',
 980000.00,
 NULL,
 '2479f157-0d26-4b62-a447-e05cdc2e1cb4'),

('d2b6e568-0f5b-42ad-b6c5-eeaaf7fbe861',
 'Greek Bronze Spearhead',
 'BHM-GRK-455',
 '1901-07-18',
 175000.00,
 NULL,
 '701d2a3f-42ab-4532-82cd-951bb3a6ea47'),

('ee6d710a-5acc-4322-b206-ffd43edafe80',
 'Renaissance Oil Portrait',
 'MET-REN-889',
 '1910-05-09',
 1450000.00,
 NULL,
 '9275c5b5-0d69-4c65-ac41-d377657f39e8'),

 ('cf459c1c-276e-49fc-b4bd-f90050db037b',
 'Ming Dynasty Porcelain Vase',
 'SHM-MNG-001',
 '1928-04-11',
 2200000.00,
 NULL,
 '61447efc-d8aa-4040-a1bc-0f3edccd5648'),

('d406b896-b63b-4b1f-a838-8bc7511303f3',
 'Qing Dynasty Jade Pendant',
 'SHM-QNG-014',
 '1936-09-23',
 480000.00,
 NULL,
 '61447efc-d8aa-4040-a1bc-0f3edccd5648'),

('2c6ca5c1-645b-4f91-bdf7-ae22184fb822',
 'Ancient Silk Road Trade Map',
 'SHM-SLK-210',
 '1905-02-17',
 1250000.00,
 NULL,
 '61447efc-d8aa-4040-a1bc-0f3edccd5648'),

('f076d0b4-06f3-4612-9c7f-fda04033bee2',
 'Han Dynasty Bronze Mirror',
 'SHM-HAN-088',
 '1912-06-30',
 760000.00,
 NULL,
 '61447efc-d8aa-4040-a1bc-0f3edccd5648'),

('9fbf5c2a-280a-4c80-82fa-233886a2a344',
 'Tang Dynasty Ceramic Horse',
 'SHM-TNG-302',
 '1899-11-05',
 990000.00,
 NULL,
 '61447efc-d8aa-4040-a1bc-0f3edccd5648');


-- ============================================
-- Loans
-- ============================================

INSERT INTO loans
(loan_id, start_date, end_date, to_museum_id, from_museum_id, loan_status, insurance_value)
VALUES
('94458865-a84d-4ed4-ab39-544f029fe60b',
 '2016-09-01',
 '2017-02-01',
 '2479f157-0d26-4b62-a447-e05cdc2e1cb4',
 '701d2a3f-42ab-4532-82cd-951bb3a6ea47',
 'Completed',
 200000.00),

('cc13670e-77e3-41b7-bd49-e8d6d86baad0',
 '2020-10-01',
 '2021-01-15',
 '11e81e1d-82c9-4b30-8c4c-e9bf702057ba',
 '9275c5b5-0d69-4c65-ac41-d377657f39e8',
 'Completed',
 1500000.00),

('cb0cd20b-4a6c-44ff-8899-c3209fc6ffae',
 '2024-05-16',
 '2026-11-30',
 '701d2a3f-42ab-4532-82cd-951bb3a6ea47',
 '9275c5b5-0d69-4c65-ac41-d377657f39e8',
 'Active',
 1000000.00),

('61e78133-3521-4a21-92e4-054d50cac842',
 '2027-04-01',
 '2027-09-30',
 '701d2a3f-42ab-4532-82cd-951bb3a6ea47',
 '2479f157-0d26-4b62-a447-e05cdc2e1cb4',
 'Scheduled',
 1000000.00),

('c157d98c-3567-4777-8259-1f3c2f9cd0e6',
 '2024-01-01',
 '2024-06-30',
 '9275c5b5-0d69-4c65-ac41-d377657f39e8',
 '11e81e1d-82c9-4b30-8c4c-e9bf702057ba',
 'Completed',
 900000.00),

('2d3b3eee-8654-4cbd-bcdf-90035d5edabe',
 '2025-03-01',
 '2025-12-31',
 '2479f157-0d26-4b62-a447-e05cdc2e1cb4',
 '701d2a3f-42ab-4532-82cd-951bb3a6ea47',
 'Active',
 1300000.00),

('dec38f13-e7e7-4cbb-9ee4-cad6e69bc867',
 '2026-05-01',
 '2026-11-01',
 '701d2a3f-42ab-4532-82cd-951bb3a6ea47',
 '9275c5b5-0d69-4c65-ac41-d377657f39e8',
 'Scheduled',
 2100000.00),

('149b38c2-ed53-4df3-8152-df0e26f761aa',
 '2019-01-15',
 '2021-08-15',
 '2479f157-0d26-4b62-a447-e05cdc2e1cb4',
 '61447efc-d8aa-4040-a1bc-0f3edccd5648',
 'Completed',
 2300000.00),

('1190ff1c-ae6d-40fb-b9db-0e6e43884891',
 '2022-03-01',
 '2026-09-01',
 '9275c5b5-0d69-4c65-ac41-d377657f39e8',
 '61447efc-d8aa-4040-a1bc-0f3edccd5648',
 'Active',
 1300000.00),

('067b03f9-0190-452d-ab1c-b8a53fabae7c',
 '2026-05-01',
 '2026-12-01',
 '61447efc-d8aa-4040-a1bc-0f3edccd5648',
 '701d2a3f-42ab-4532-82cd-951bb3a6ea47',
 'Scheduled',
 1400000.00);


-- ============================================
-- artifact_loans (Many-to-Many)
-- ============================================

INSERT INTO artifact_loans
(artifact_id, loan_id, display_requirements, return_condition_required)
VALUES
-- Loan 1 (Samurai set)
('76b05424-a679-4e6f-9788-a73a0c137297',
 'c157d98c-3567-4777-8259-1f3c2f9cd0e6',
 'Climate controlled display, humidity < 50%',
 'No corrosion or structural damage'),

('ffb5f8e2-0677-4bc2-890f-c6f48d6893fb',
 'c157d98c-3567-4777-8259-1f3c2f9cd0e6',
 'Low light exposure, secure mounting',
 'No dents or lacquer deterioration'),

('f6665a95-25d7-492d-8114-f9527de168bd',
 'c157d98c-3567-4777-8259-1f3c2f9cd0e6',
 'Climate controlled display case',
 'No cracking or metal fatigue'),

-- Loan 2 (Roman bust)
('23230050-202b-47b4-88b1-a67756706623',
 '2d3b3eee-8654-4cbd-bcdf-90035d5edabe',
 'Pedestal display with vibration isolation',
 'No surface chipping'),

-- Loan 3 (Sarcophagus)
('ac83f5d8-b4c4-449b-803a-03c5d4c7e17e',
 'dec38f13-e7e7-4cbb-9ee4-cad6e69bc867',
 'Reinforced flooring, 24hr security monitoring',
 'No structural cracks or pigment loss'),

-- Greek Spearhead loaned to Louvre
('d2b6e568-0f5b-42ad-b6c5-eeaaf7fbe861',
 '94458865-a84d-4ed4-ab39-544f029fe60b',
 'Sealed display case with humidity control',
 'No new oxidation or structural stress'),

-- Renaissance Portrait loaned to Tokyo
('ee6d710a-5acc-4322-b206-ffd43edafe80',
 'cc13670e-77e3-41b7-bd49-e8d6d86baad0',
 'Low light exposure (<50 lux), secure wall mounting',
 'No pigment flaking or canvas warping'),

-- Medieval Manuscript loaned twice
('391352cb-1b64-4a69-a76e-175aa923e095',
 'cb0cd20b-4a6c-44ff-8899-c3209fc6ffae',
 'Temperature-controlled glass case',
 'No binding deterioration or page tears'),
 
('391352cb-1b64-4a69-a76e-175aa923e095',
 '61e78133-3521-4a21-92e4-054d50cac842',
 'Temperature-controlled glass case',
 'No binding deterioration or page tears'),

-- Ming Vase to Louvre
('cf459c1c-276e-49fc-b4bd-f90050db037b',
 '149b38c2-ed53-4df3-8152-df0e26f761aa',
 'Glass enclosure with vibration monitoring',
 'No glaze cracking or chipping'),

-- Silk Road Map to MET
('2c6ca5c1-645b-4f91-bdf7-ae22184fb822',
 '1190ff1c-ae6d-40fb-b9db-0e6e43884891',
 'Low light exposure (<30 lux), climate control',
 'No additional fraying or ink fading'),

-- Roman Bust loaned to Shanghai (existing artifact)
('23230050-202b-47b4-88b1-a67756706623',
 '067b03f9-0190-452d-ab1c-b8a53fabae7c',
 'Pedestal with seismic stabilizer',
 'No surface abrasions or new fractures');



-- ============================================
-- Condition Reports
-- ============================================

INSERT INTO condition_reports
(report_id, artifact_id, report_date, condition_rating, notes)
VALUES
('afe8d71c-1a8c-424f-b672-db88e8600f76',
 '76b05424-a679-4e6f-9788-a73a0c137297',
 '2023-12-01',
 9,
 'Excellent condition. Minor surface aging consistent with period.'),

('021d41a9-94e9-4491-8a6d-352e2b168cbd',
 'ffb5f8e2-0677-4bc2-890f-c6f48d6893fb',
 '2023-12-01',
 8,
 'Light lacquer wear on crest. Structurally stable.'),

('4ecaa4e1-09a0-458e-bcf0-49f2004fae44',
 'ac83f5d8-b4c4-449b-803a-03c5d4c7e17e',
 '2025-02-15',
 7,
 'Small pigment fading on lid. No structural damage.'),

('b5ecf47d-0643-4cd8-a8e2-a76db48d202d',
 '23230050-202b-47b4-88b1-a67756706623',
 '2025-02-20',
 9,
 'Surface cleaned and restored. No visible cracks.'),

('2fe25b25-4f13-4f98-8145-58d7cc9abc27',
 '391352cb-1b64-4a69-a76e-175aa923e095',
 '2024-08-10',
 8,
 'Pages intact. Slight binding stress noted.'),

 ('f82efb23-2327-4315-a708-adc0d9b183b9',
 'd2b6e568-0f5b-42ad-b6c5-eeaaf7fbe861',
 '2025-01-12',
 8,
 'Minor surface oxidation. Stable structural integrity.'),

('3e4f39b2-8e50-45dd-86b0-556e2ff4826d',
 'd2b6e568-0f5b-42ad-b6c5-eeaaf7fbe861',
 '2026-01-10',
 9,
 'Conservation treatment completed. Oxidation reduced.'),

('85a11a23-d2ad-4ed3-88f4-2f1698f3f19d',
 'ee6d710a-5acc-4322-b206-ffd43edafe80',
 '2025-03-22',
 7,
 'Small varnish discoloration in upper corner.'),

('feb31d36-70e4-4c59-87b6-ffbad855d36c',
 'ee6d710a-5acc-4322-b206-ffd43edafe80',
 '2026-03-18',
 8,
 'Surface cleaned. Pigment stable. Frame reinforced.'),

('df46a65a-4782-4c2d-b5d7-659308d09d9e',
 'cf459c1c-276e-49fc-b4bd-f90050db037b',
 '2025-04-01',
 9,
 'Excellent glaze preservation. No visible cracks.'),

('e225f4e9-a429-4258-a989-440d7ac468eb',
 'd406b896-b63b-4b1f-a838-8bc7511303f3',
 '2025-04-02',
 8,
 'Minor surface wear. Carving details remain sharp.'),

('7f23c459-a138-4df1-a00b-2e354ca402f3',
 '2c6ca5c1-645b-4f91-bdf7-ae22184fb822',
 '2025-04-03',
 7,
 'Edges slightly frayed. Ink stable and legible.'),

('28cd3c59-dd12-4aaf-aabc-080b2e5d2ab4',
 'f076d0b4-06f3-4612-9c7f-fda04033bee2',
 '2025-04-04',
 8,
 'Patina consistent with age. No structural warping.'),

('e8c68fd7-5711-427a-9718-863fd41ae43f',
 '9fbf5c2a-280a-4c80-82fa-233886a2a344',
 '2025-04-05',
 9,
 'Excellent structural stability. Surface intact.');

-- ============================================
-- Constraints on Artifact Loan
-- ============================================


ALTER TABLE artifact_loans DROP CONSTRAINT artifact_loans_artifact_id_fkey;
ALTER TABLE artifact_loans DROP CONSTRAINT artifact_loans_loan_id_fkey;
ALTER TABLE condition_reports DROP CONSTRAINT condition_reports_artifact_id_fkey;


ALTER TABLE artifact_loans 
ADD CONSTRAINT artifact_loans_artifact_id_fkey
FOREIGN KEY (artifact_id)
REFERENCES artifacts(artifact_id)
ON DELETE CASCADE;

ALTER TABLE artifact_loans 
ADD CONSTRAINT artifact_loans_loan_id_fkey
FOREIGN KEY (loan_id)
REFERENCES loans(loan_id)
ON DELETE CASCADE;


ALTER TABLE condition_reports 
ADD CONSTRAINT condition_reports_artifact_id_fkey
FOREIGN KEY (artifact_id)
REFERENCES artifacts(artifact_id)
ON DELETE CASCADE;

select * from loans;
select * from condition_reports;
select * from artifacts;
select * from artifact_loans;
select * from museums;