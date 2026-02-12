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
('bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb',
 'Samurai Helmet (Kabuto)',
 'TNM-ARM-001-H',
 '1856-04-12',
 250000.00,
 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
 '44444444-4444-4444-4444-444444444444'),

('cccccccc-cccc-cccc-cccc-cccccccccccc',
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
('dddddddd-dddd-dddd-dddd-dddddddddddd',
 'Ancient Egyptian Sarcophagus',
 'MET-EGY-778',
 '1922-11-04',
 2000000.00,
 NULL,
 '11111111-1111-1111-1111-111111111111'),

('eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee',
 'Roman Marble Bust of Caesar',
 'BHM-ROM-102',
 '1898-06-21',
 1250000.00,
 NULL,
 '22222222-2222-2222-2222-222222222222'),

('ffffffff-ffff-ffff-ffff-ffffffffffff',
 'Medieval Illuminated Manuscript',
 'LOU-MED-334',
 '1875-03-15',
 980000.00,
 NULL,
 '33333333-3333-3333-3333-333333333333');


-- ============================================
-- Loans
-- ============================================

INSERT INTO loans
(loan_id, start_date, end_date, to_museum_id, from_museum_id, loan_status, insurance_value)
VALUES
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

('bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb',
 '99999999-9999-9999-9999-999999999991',
 'Low light exposure, secure mounting',
 'No dents or lacquer deterioration'),

('cccccccc-cccc-cccc-cccc-cccccccccccc',
 '99999999-9999-9999-9999-999999999991',
 'Climate controlled display case',
 'No cracking or metal fatigue'),

-- Loan 2 (Roman bust)
('eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee',
 '99999999-9999-9999-9999-999999999992',
 'Pedestal display with vibration isolation',
 'No surface chipping'),

-- Loan 3 (Sarcophagus)
('dddddddd-dddd-dddd-dddd-dddddddddddd',
 '99999999-9999-9999-9999-999999999993',
 'Reinforced flooring, 24hr security monitoring',
 'No structural cracks or pigment loss');


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
 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb',
 '2023-12-01',
 8,
 'Light lacquer wear on crest. Structurally stable.'),

('aaaaaaaa-0000-0000-0000-000000000003',
 'dddddddd-dddd-dddd-dddd-dddddddddddd',
 '2025-02-15',
 7,
 'Small pigment fading on lid. No structural damage.'),

('aaaaaaaa-0000-0000-0000-000000000004',
 'eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee',
 '2025-02-20',
 9,
 'Surface cleaned and restored. No visible cracks.'),

('aaaaaaaa-0000-0000-0000-000000000005',
 'ffffffff-ffff-ffff-ffff-ffffffffffff',
 '2024-08-10',
 8,
 'Pages intact. Slight binding stress noted.');

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



select * from artifacts;