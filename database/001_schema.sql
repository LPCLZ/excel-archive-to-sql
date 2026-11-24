-- Stores the names of project beneficiaries.
CREATE TABLE beneficiaries
(
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    beneficiary_name TEXT NOT NULL
);

-- Lists the types of services available for a project.
CREATE TABLE services
(
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    service_type TEXT NOT NULL CHECK
    (
        service_type IN ('Studiu Solutie', 'Servicii Consultanta', 'Proiectare Electrica')
    ),
    UNIQUE (service_type)
);

-- Stores project names and types.
CREATE TABLE projects 
(
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    project_name TEXT NOT NULL,
    project_type TEXT CHECK
    (
        project_type IN ('CEF', 'CEM', 'CEE', 'IS', 'CHEAP','DATACENTER')
    )                                       
);

-- Links projects to beneficiaries, with one row per project and beneficiary pair.
CREATE TABLE project_beneficiaries
(
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    beneficiary_id INTEGER NOT NULL REFERENCES beneficiaries(id),
    project_id INTEGER NOT NULL REFERENCES projects(id),
    UNIQUE (project_id, beneficiary_id)
);

-- Records which services are associated with each project.
CREATE TABLE project_services
(
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    project_id INTEGER NOT NULL REFERENCES projects(id),
    service_id INTEGER NOT NULL REFERENCES services(id),
    UNIQUE (project_id, service_id)
);

-- Lists the legal entities that issue documents.
CREATE TABLE entities
(
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    entity_name TEXT NOT NULL CHECK
    (
        entity_name IN ('A.B. INTELIGENT AX SRL' , 'A.B. INTELIGENT LM SRL')
    ),
    UNIQUE (entity_name)
);

-- Stores document's type, number, date, and issuing entity.
CREATE TABLE documents
(
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    entity_id INTEGER NOT NULL REFERENCES entities(id),
    document_type TEXT NOT NULL,
    document_number TEXT,
    document_date DATE

);

-- Links each document to the project it covers.
CREATE TABLE document_projects
(
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    document_id INTEGER NOT NULL REFERENCES documents(id),
    project_id INTEGER NOT NULL REFERENCES projects(id),
    UNIQUE (document_id, project_id)
);