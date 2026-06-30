
CREATE TABLE IF NOT EXISTS employee_master (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id TEXT,
    employee_name TEXT,
    department TEXT,
    experience_years INTEGER,
    salary INTEGER,
    performance_rating INTEGER,
    attendance_percent INTEGER,
    certification TEXT,
    location TEXT
);


CREATE TABLE IF NOT EXISTS payroll_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id TEXT,
    salary INTEGER,
    performance_score INTEGER,
    department TEXT,
    bonus_percent REAL,
    bonus_amount INTEGER,
    scholarship INTEGER,
    tax REAL,
    net_salary REAL,
    performance_grade TEXT,
    promotion TEXT,
    reward TEXT,
    experience_level TEXT
);

