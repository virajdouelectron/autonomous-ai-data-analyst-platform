CREATE TABLE IF NOT EXISTS datasets (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  filename TEXT NOT NULL,
  rows INTEGER,
  columns INTEGER,
  column_names JSONB,
  data JSONB,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS insights (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  dataset_id UUID REFERENCES datasets(id),
  prompt TEXT,
  response TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS models (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  dataset_id UUID REFERENCES datasets(id),
  target_column TEXT,
  model_type TEXT,
  metrics JSONB,
  created_at TIMESTAMP DEFAULT NOW()
);