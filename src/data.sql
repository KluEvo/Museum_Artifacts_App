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
('44444444-4444-4444-4444-444444444444', 'Tokyo National Museum', 'Tokyo, Japan', 'admin@tnm.jp');

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

('12121212-1212-1212-1212-121212121212',
 'Greek Bronze Spearhead',
 'BHM-GRK-455',
 '1901-07-18',
 175000.00,
 NULL,
 '22222222-2222-2222-2222-222222222222'),

('34343434-3434-3434-3434-343434343434',
 'Renaissance Oil Portrait',
 'MET-REN-889',
 '1910-05-09',
 1450000.00,
 NULL,
 '11111111-1111-1111-1111-111111111111');


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
 2100000.00);


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
('12121212-1212-1212-1212-121212121212',
 '88888888-8888-8888-8888-888888888881',
 'Sealed display case with humidity control',
 'No new oxidation or structural stress'),

-- Renaissance Portrait loaned to Tokyo
('34343434-3434-3434-3434-343434343434',
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
 'No binding deterioration or page tears');



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
 '12121212-1212-1212-1212-121212121212',
 '2025-01-12',
 8,
 'Minor surface oxidation. Stable structural integrity.'),

('abababab-0000-0000-0000-000000000002',
 '12121212-1212-1212-1212-121212121212',
 '2026-01-10',
 9,
 'Conservation treatment completed. Oxidation reduced.'),

('cdcdcdcd-0000-0000-0000-000000000001',
 '34343434-3434-3434-3434-343434343434',
 '2025-03-22',
 7,
 'Small varnish discoloration in upper corner.'),

('cdcdcdcd-0000-0000-0000-000000000002',
 '34343434-3434-3434-3434-343434343434',
 '2026-03-18',
 8,
 'Surface cleaned. Pigment stable. Frame reinforced.');

-- ============================================
-- Constraints on Artifact Loan
-- ============================================

ALTER TABLE artifact_loans 
ADD CONSTRAINT artifact_id_fk_removal
FOREIGN KEY (artifact_id)
REFERENCES artifacts(artifact_id)
ON DELETE CASCADE;

ALTER TABLE artifact_loans 
ADD CONSTRAINT loan_id_fk_removal
FOREIGN KEY (loan_id)
REFERENCES loans(loan_id)
ON DELETE CASCADE;



select * from loans;
select * from artifacts;
select * from artifact_loans;