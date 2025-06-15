-- Data Cleaning SQL Queries

-- Remove invalid daily activity records
DELETE FROM daily_activity 
WHERE TotalSteps < 0 
   OR TotalDistance < 0 
   OR Calories < 0 
   OR SedentaryMinutes < 0 
   OR LightlyActiveMinutes < 0 
   OR FairlyActiveMinutes < 0 
   OR VeryActiveMinutes < 0 
   OR ActivityCalories < 0;

-- Remove invalid daily intensities records
DELETE FROM daily_intensities 
WHERE SedentaryMinutes < 0 
   OR LightlyActiveMinutes < 0 
   OR FairlyActiveMinutes < 0 
   OR VeryActiveMinutes < 0;

-- Remove invalid daily steps records
DELETE FROM daily_steps 
WHERE StepTotal < 0;

-- Remove invalid weight records
DELETE FROM weight_log 
WHERE Weight < 0 
   OR BMI < 0;

-- Remove invalid minute steps records
DELETE FROM minute_steps 
WHERE Steps < 0;

-- Remove invalid heart rate records
DELETE FROM heart_rate 
WHERE Value < 0 
   OR Value > 200;  -- Maximum reasonable heart rate

-- Remove duplicate records
DELETE FROM daily_activity 
WHERE rowid NOT IN (
    SELECT MIN(rowid) 
    FROM daily_activity 
    GROUP BY Id, ActivityDate
);

DELETE FROM daily_intensities 
WHERE rowid NOT IN (
    SELECT MIN(rowid) 
    FROM daily_intensities 
    GROUP BY Id, ActivityDay
);

DELETE FROM daily_steps 
WHERE rowid NOT IN (
    SELECT MIN(rowid) 
    FROM daily_steps 
    GROUP BY Id, ActivityDay
);

DELETE FROM weight_log 
WHERE rowid NOT IN (
    SELECT MIN(rowid) 
    FROM weight_log 
    GROUP BY Id, Date
);

DELETE FROM minute_steps 
WHERE rowid NOT IN (
    SELECT MIN(rowid) 
    FROM minute_steps 
    GROUP BY Id, Time
);

DELETE FROM heart_rate 
WHERE rowid NOT IN (
    SELECT MIN(rowid) 
    FROM heart_rate 
    GROUP BY Id, Time
);

-- Add indexes for better performance
CREATE INDEX IF NOT EXISTS idx_daily_activity_date ON daily_activity(ActivityDate);
CREATE INDEX IF NOT EXISTS idx_daily_intensities_day ON daily_intensities(ActivityDay);
CREATE INDEX IF NOT EXISTS idx_daily_steps_day ON daily_steps(ActivityDay);
CREATE INDEX IF NOT EXISTS idx_weight_log_date ON weight_log(Date);
CREATE INDEX IF NOT EXISTS idx_minute_steps_time ON minute_steps(Time);
CREATE INDEX IF NOT EXISTS idx_heart_rate_time ON heart_rate(Time);

-- Add constraints
ALTER TABLE daily_activity 
ADD CONSTRAINT chk_steps CHECK (TotalSteps >= 0);

ALTER TABLE daily_intensities 
ADD CONSTRAINT chk_minutes CHECK (SedentaryMinutes >= 0 
    AND LightlyActiveMinutes >= 0 
    AND FairlyActiveMinutes >= 0 
    AND VeryActiveMinutes >= 0);

ALTER TABLE daily_steps 
ADD CONSTRAINT chk_step_total CHECK (StepTotal >= 0);

ALTER TABLE weight_log 
ADD CONSTRAINT chk_weight CHECK (Weight >= 0 
    AND BMI >= 0);

ALTER TABLE minute_steps 
ADD CONSTRAINT chk_minute_steps CHECK (Steps >= 0);

ALTER TABLE heart_rate 
ADD CONSTRAINT chk_heart_rate CHECK (Value >= 0 
    AND Value <= 200);
