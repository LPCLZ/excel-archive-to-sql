SELECT projects.project_name, beneficiaries.beneficiary_name
FROM beneficiaries
JOIN project_beneficiaries 
ON beneficiaries.id = project_beneficiaries.beneficiary_id
JOIN projects
ON project_beneficiaries.project_id = projects.id;