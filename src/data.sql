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
('11111111-1111-1111-1111-111111111111', 'Metropolitan Museum of History', 'New York, USA', 'contact@metmuseum.org'),
('22222222-2222-2222-2222-222222222222', 'British Heritage Museum', 'London, UK', 'info@britishheritage.uk'),
('33333333-3333-3333-3333-333333333333', 'Louvre Antiquities Wing', 'Paris, France', 'collections@louvre.fr'),
('44444444-4444-4444-4444-444444444444', 'Tokyo National Museum', 'Tokyo, Japan', 'admin@tnm.jp'),
('55555555-5555-5555-5555-555555555555', 'Shanghai Museum', 'Shanghai, China', 'service@shanghaimuseum.cn');

-- ============================================
-- Artifacts
-- ============================================

-- Parent artifact (Armor Set)
INSERT INTO artifacts 
(artifact_id, name, accession_number, discovery_date, estimated_value, parent_artifact, museum_id)
VALUES
('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
 'Samurai Armor Set',
 'TNM-ARM-001',
 '1856-04-12',
 850000.00,
 NULL,
 '44444444-4444-4444-4444-444444444444');

-- Child artifacts (self-referencing)
INSERT INTO artifacts 
(artifact_id, name, accession_number, discovery_date, estimated_value, parent_artifact, museum_id)
VALUES
('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaab',
 'Samurai Helmet (Kabuto)',
 'TNM-ARM-001-H',
 '1856-04-12',
 250000.00,
 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
 '44444444-4444-4444-4444-444444444444'),

('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaac',
 'Samurai Chest Plate',
 'TNM-ARM-001-C',
 '1856-04-12',
 300000.00,
 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
 '44444444-4444-4444-4444-444444444444');

-- Independent artifacts
INSERT INTO artifacts 
(artifact_id, name, accession_number, discovery_date, estimated_value, parent_artifact, museum_id)
VALUES
('aaaaaaaa-aaaa-aaaa-aaaa-daaaaaaaaaaa',
 'Ancient Egyptian Sarcophagus',
 'MET-EGY-778',
 '1922-11-04',
 2000000.00,
 NULL,
 '11111111-1111-1111-1111-111111111111'),

('aaaaaaaa-aaaa-aaaa-aaaa-eaaaaaaaaaaa',
 'Roman Marble Bust of Caesar',
 'BHM-ROM-102',
 '1898-06-21',
 1250000.00,
 NULL,
 '22222222-2222-2222-2222-222222222222'),

('aaaaaaaa-aaaa-aaaa-aaaa-faaaaaaaaaaa',
 'Medieval Illuminated Manuscript',
 'LOU-MED-334',
 '1875-03-15',
 980000.00,
 NULL,
 '33333333-3333-3333-3333-333333333333'),

('aaaaaaaa-aaaa-aaaa-aaaa-0aaaaaaaaaaa',
 'Greek Bronze Spearhead',
 'BHM-GRK-455',
 '1901-07-18',
 175000.00,
 NULL,
 '22222222-2222-2222-2222-222222222222'),

('aaaaaaaa-aaaa-aaaa-aaaa-0baaaaaaaaaa',
 'Renaissance Oil Portrait',
 'MET-REN-889',
 '1910-05-09',
 1450000.00,
 NULL,
 '11111111-1111-1111-1111-111111111111'),

 ('aaaaaaaa-aaaa-aaaa-aaaa-5aaaaaaaaaaa',
 'Ming Dynasty Porcelain Vase',
 'SHM-MNG-001',
 '1928-04-11',
 2200000.00,
 NULL,
 '55555555-5555-5555-5555-555555555555'),

('aaaaaaaa-aaaa-aaaa-aaaa-5baaaaaaaaaa',
 'Qing Dynasty Jade Pendant',
 'SHM-QNG-014',
 '1936-09-23',
 480000.00,
 NULL,
 '55555555-5555-5555-5555-555555555555'),

('aaaaaaaa-aaaa-aaaa-aaaa-5caaaaaaaaaa',
 'Ancient Silk Road Trade Map',
 'SHM-SLK-210',
 '1905-02-17',
 1250000.00,
 NULL,
 '55555555-5555-5555-5555-555555555555'),

('aaaaaaaa-aaaa-aaaa-aaaa-5daaaaaaaaaa',
 'Han Dynasty Bronze Mirror',
 'SHM-HAN-088',
 '1912-06-30',
 760000.00,
 NULL,
 '55555555-5555-5555-5555-555555555555'),

('aaaaaaaa-aaaa-aaaa-aaaa-5eaaaaaaaaaa',
 'Tang Dynasty Ceramic Horse',
 'SHM-TNG-302',
 '1899-11-05',
 990000.00,
 NULL,
 '55555555-5555-5555-5555-555555555555');


-- ============================================
-- Loans
-- ============================================

INSERT INTO loans
(loan_id, start_date, end_date, to_museum_id, from_museum_id, loan_status, insurance_value)
VALUES
('88888888-8888-8888-8888-888888888881',
 '2016-09-01',
 '2017-02-01',
 '33333333-3333-3333-3333-333333333333',
 '22222222-2222-2222-2222-222222222222',
 'Completed',
 200000.00),

('88888888-8888-8888-8888-888888888882',
 '2020-10-01',
 '2021-01-15',
 '44444444-4444-4444-4444-444444444444',
 '11111111-1111-1111-1111-111111111111',
 'Completed',
 1500000.00),

('88888888-8888-8888-8888-888888888883',
 '2024-05-16',
 '2026-11-30',
 '22222222-2222-2222-2222-222222222222',
 '11111111-1111-1111-1111-111111111111',
 'Active',
 1000000.00),

('88888888-8888-8888-8888-888888888884',
 '2027-04-01',
 '2027-09-30',
 '22222222-2222-2222-2222-222222222222',
 '33333333-3333-3333-3333-333333333333',
 'Scheduled',
 1000000.00),

('99999999-9999-9999-9999-999999999991',
 '2024-01-01',
 '2024-06-30',
 '11111111-1111-1111-1111-111111111111',
 '44444444-4444-4444-4444-444444444444',
 'Completed',
 900000.00),

('99999999-9999-9999-9999-999999999992',
 '2025-03-01',
 '2025-12-31',
 '33333333-3333-3333-3333-333333333333',
 '22222222-2222-2222-2222-222222222222',
 'Active',
 1300000.00),

('99999999-9999-9999-9999-999999999993',
 '2026-05-01',
 '2026-11-01',
 '22222222-2222-2222-2222-222222222222',
 '11111111-1111-1111-1111-111111111111',
 'Scheduled',
 2100000.00),

-- Outgoing: Ming Vase to Louvre
('77777777-7777-7777-7777-777777777771',
 '2019-01-15',
 '2021-08-15',
 '33333333-3333-3333-3333-333333333333',
 '55555555-5555-5555-5555-555555555555',
 'Completed',
 2300000.00),

-- Outgoing: Silk Road Map to Metropolitan Museum
('77777777-7777-7777-7777-777777777772',
 '2022-03-01',
 '2026-09-01',
 '11111111-1111-1111-1111-111111111111',
 '55555555-5555-5555-5555-555555555555',
 'Active',
 1300000.00),

-- Incoming: Roman Bust from British Heritage Museum
('77777777-7777-7777-7777-777777777773',
 '2026-05-01',
 '2026-12-01',
 '55555555-5555-5555-5555-555555555555',
 '22222222-2222-2222-2222-222222222222',
 'Scheduled',
 1400000.00);


-- ============================================
-- artifact_loans (Many-to-Many)
-- ============================================

INSERT INTO artifact_loans
(artifact_id, loan_id, display_requirements, return_condition_required)
VALUES
-- Loan 1 (Samurai set)
('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
 '99999999-9999-9999-9999-999999999991',
 'Climate controlled display, humidity < 50%',
 'No corrosion or structural damage'),

('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaab',
 '99999999-9999-9999-9999-999999999991',
 'Low light exposure, secure mounting',
 'No dents or lacquer deterioration'),

('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaac',
 '99999999-9999-9999-9999-999999999991',
 'Climate controlled display case',
 'No cracking or metal fatigue'),

-- Loan 2 (Roman bust)
('aaaaaaaa-aaaa-aaaa-aaaa-eaaaaaaaaaaa',
 '99999999-9999-9999-9999-999999999992',
 'Pedestal display with vibration isolation',
 'No surface chipping'),

-- Loan 3 (Sarcophagus)
('aaaaaaaa-aaaa-aaaa-aaaa-daaaaaaaaaaa',
 '99999999-9999-9999-9999-999999999993',
 'Reinforced flooring, 24hr security monitoring',
 'No structural cracks or pigment loss'),

-- Greek Spearhead loaned to Louvre
('aaaaaaaa-aaaa-aaaa-aaaa-0aaaaaaaaaaa',
 '88888888-8888-8888-8888-888888888881',
 'Sealed display case with humidity control',
 'No new oxidation or structural stress'),

-- Renaissance Portrait loaned to Tokyo
('aaaaaaaa-aaaa-aaaa-aaaa-0baaaaaaaaaa',
 '88888888-8888-8888-8888-888888888882',
 'Low light exposure (<50 lux), secure wall mounting',
 'No pigment flaking or canvas warping'),

-- Medieval Manuscript loaned twice
('aaaaaaaa-aaaa-aaaa-aaaa-faaaaaaaaaaa',
 '88888888-8888-8888-8888-888888888883',
 'Temperature-controlled glass case',
 'No binding deterioration or page tears'),
 
('aaaaaaaa-aaaa-aaaa-aaaa-faaaaaaaaaaa',
 '88888888-8888-8888-8888-888888888884',
 'Temperature-controlled glass case',
 'No binding deterioration or page tears'),

-- Ming Vase to Louvre
('aaaaaaaa-aaaa-aaaa-aaaa-5aaaaaaaaaaa',
 '77777777-7777-7777-7777-777777777771',
 'Glass enclosure with vibration monitoring',
 'No glaze cracking or chipping'),

-- Silk Road Map to MET
('aaaaaaaa-aaaa-aaaa-aaaa-5caaaaaaaaaa',
 '77777777-7777-7777-7777-777777777772',
 'Low light exposure (<30 lux), climate control',
 'No additional fraying or ink fading'),

-- Roman Bust loaned to Shanghai (existing artifact)
('aaaaaaaa-aaaa-aaaa-aaaa-eaaaaaaaaaaa',
 '77777777-7777-7777-7777-777777777773',
 'Pedestal with seismic stabilizer',
 'No surface abrasions or new fractures');



-- ============================================
-- Condition Reports
-- ============================================

INSERT INTO condition_reports
(report_id, artifact_id, report_date, condition_rating, notes)
VALUES
('aaaaaaaa-0000-0000-0000-000000000001',
 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
 '2023-12-01',
 9,
 'Excellent condition. Minor surface aging consistent with period.'),

('aaaaaaaa-0000-0000-0000-000000000002',
 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaab',
 '2023-12-01',
 8,
 'Light lacquer wear on crest. Structurally stable.'),

('aaaaaaaa-0000-0000-0000-000000000003',
 'aaaaaaaa-aaaa-aaaa-aaaa-daaaaaaaaaaa',
 '2025-02-15',
 7,
 'Small pigment fading on lid. No structural damage.'),

('aaaaaaaa-0000-0000-0000-000000000004',
 'aaaaaaaa-aaaa-aaaa-aaaa-eaaaaaaaaaaa',
 '2025-02-20',
 9,
 'Surface cleaned and restored. No visible cracks.'),

('aaaaaaaa-0000-0000-0000-000000000005',
 'aaaaaaaa-aaaa-aaaa-aaaa-faaaaaaaaaaa',
 '2024-08-10',
 8,
 'Pages intact. Slight binding stress noted.'),

 ('abababab-0000-0000-0000-000000000001',
 'aaaaaaaa-aaaa-aaaa-aaaa-0aaaaaaaaaaa',
 '2025-01-12',
 8,
 'Minor surface oxidation. Stable structural integrity.'),

('abababab-0000-0000-0000-000000000002',
 'aaaaaaaa-aaaa-aaaa-aaaa-0aaaaaaaaaaa',
 '2026-01-10',
 9,
 'Conservation treatment completed. Oxidation reduced.'),

('cdcdcdcd-0000-0000-0000-000000000001',
 'aaaaaaaa-aaaa-aaaa-aaaa-0baaaaaaaaaa',
 '2025-03-22',
 7,
 'Small varnish discoloration in upper corner.'),

('cdcdcdcd-0000-0000-0000-000000000002',
 'aaaaaaaa-aaaa-aaaa-aaaa-0baaaaaaaaaa',
 '2026-03-18',
 8,
 'Surface cleaned. Pigment stable. Frame reinforced.'),

('aaaa5555-0000-0000-0000-000000000001',
 'aaaaaaaa-aaaa-aaaa-aaaa-5aaaaaaaaaaa',
 '2025-04-01',
 9,
 'Excellent glaze preservation. No visible cracks.'),

('aaaa5555-0000-0000-0000-000000000002',
 'aaaaaaaa-aaaa-aaaa-aaaa-5baaaaaaaaaa',
 '2025-04-02',
 8,
 'Minor surface wear. Carving details remain sharp.'),

('aaaa5555-0000-0000-0000-000000000003',
 'aaaaaaaa-aaaa-aaaa-aaaa-5caaaaaaaaaa',
 '2025-04-03',
 7,
 'Edges slightly frayed. Ink stable and legible.'),

('aaaa5555-0000-0000-0000-000000000004',
 'aaaaaaaa-aaaa-aaaa-aaaa-5daaaaaaaaaa',
 '2025-04-04',
 8,
 'Patina consistent with age. No structural warping.'),

('aaaa5555-0000-0000-0000-000000000005',
 'aaaaaaaa-aaaa-aaaa-aaaa-5eaaaaaaaaaa',
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