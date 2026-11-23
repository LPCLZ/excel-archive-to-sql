SELECT projects.project_name, beneficiaries.beneficiary_name
FROM beneficiaries
JOIN projects
ON projects.beneficiary_id = beneficiaries.id;