-- Tabel beneficiari cu nume si id numeric
CREATE TABLE beneficiaries
(
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    beneficiary_name TEXT NOT NULL
);

-- Tabel cu serviciile care pot fii prestate de catre AB Energy
CREATE TABLE services
(
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    service_type TEXT NOT NULL CHECK
    (
        service_type IN ('Studiu Solutie', 'Servicii Consultanta', 'Proiectare Electrica')
    ),
    UNIQUE (service_type)
);

-- Tabel proiecte cu nume id numeric si beneficiari
CREATE TABLE projects 
(
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    project_name TEXT NOT NULL,
    project_type TEXT CHECK
    (
        project_type IN ('CEF', 'CEM', 'CEE', 'IS', 'CHEAP','DATACENTER')
    ),
    beneficiary_id INTEGER NOT NULL REFERENCES beneficiaries(id)
);

CREATE TABLE project_beneficiaries
(
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    beneficiary_id INTEGER NOT NULL REFERENCES beneficiaries(id),
    project_id INTEGER NOT NULL REFERENCES projects(id),
    UNIQUE (project_id, beneficiary_id)
);

CREATE TABLE project_services
(
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    project_id INTEGER NOT NULL REFERENCES projects(id),
    service_id INTEGER NOT NULL REFERENCES services(id),
    UNIQUE (project_id, service_id)
);

-- Tabel cu entitatile AB Energy ca sa stiu facturile pe care entitate au fost emise
CREATE TABLE entities
(
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    entity_name TEXT NOT NULL CHECK
    (
        entity_name IN ('A.B. INTELIGENT AX SRL' , 'A.B. INTELIGENT LM SRL')
    ),
    UNIQUE (entity_name)
);

-- Tabel contracte cu relatie la proiecte (pot fi mai multe contracte pe un singur proiect) cu tip, status, numar, data, subtip
CREATE TABLE documents
(
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    entity_id INTEGER NOT NULL REFERENCES entities(id),
    document_type TEXT NOT NULL,
    document_number TEXT,
    document_date DATE

);

CREATE TABLE document_projects
(
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    document_id INTEGER NOT NULL REFERENCES documents(id),
    project_id INTEGER NOT NULL REFERENCES projects(id),
    UNIQUE (document_id, project_id)
);