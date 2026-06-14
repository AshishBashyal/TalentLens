INSERT INTO job_sources (name, base_url, collection_method)
VALUES
    ('LinkedIn', 'https://www.linkedin.com/jobs', 'planned'),
    ('Indeed', 'https://www.indeed.com', 'planned'),
    ('Wellfound', 'https://wellfound.com/jobs', 'planned'),
    ('Internshala', 'https://internshala.com', 'planned'),
    ('Naukri', 'https://www.naukri.com', 'planned')
ON CONFLICT (name) DO NOTHING;

