
CREATE TABLE user (
    id VARCHAR(36) NOT NULL,
    name VARCHAR(255) NOT NULL,
    login VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,

    PRIMARY KEY (id)
);

CREATE TABLE exercise(
    id VARCHAR(36) NOT NULL,
    name VARCHAR(255) NOT NULL,
    created_by_id VARCHAR(36) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    modified_at TIMESTAMP NOT NULL DEFAULT NOW(),

    exercise_type VARCHAR(255) NOT NULL,
    body_type VARCHAR(255) NOT NULL,

    PRIMARY KEY (id),
    FOREIGN KEY (created_by_id) REFERENCES user(id)
);

CREATE TABLE workout_plan(
    id VARCHAR(36) NOT NULL,
    name VARCHAR(255) NOT NULL,
    created_by_id VARCHAR(36) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    modified_at TIMESTAMP NOT NULL DEFAULT NOW(),

    start_date TIMESTAMP NOT NULL DEFAULT NOW(),
    end_date TIMESTAMP NULL DEFAULT NULL,

    PRIMARY KEY (id)
);

CREATE TABLE exercise_plan(
    exercise_id VARCHAR(36) NOT NULL,
    workout_plan_id VARCHAR(36) NOT NULL,
    start_date TIMESTAMP NOT NULL DEFAULT NOW(),
    sets INT NOT NULL,
    repetitions INT NOT NULL,
    weight FLOAT NOT NULL,

    PRIMARY KEY (exercise_id, workout_plan_id),
    FOREIGN KEY (exercise_id) REFERENCES exercise(id),
    FOREIGN KEY (workout_plan_id) REFERENCES workout_plan(id) ON DELETE CASCADE
);

CREATE TABLE history_exercise_plan(
    exercise_id VARCHAR(36) NOT NULL,
    workout_plan_id VARCHAR(36) NOT NULL,
    start_date TIMESTAMP NOT NULL DEFAULT NOW(),
    sets INT NOT NULL,
    repetitions INT NOT NULL,
    weight FLOAT NOT NULL,

    PRIMARY KEY (exercise_id, workout_plan_id, start_date),
    FOREIGN KEY (exercise_id) REFERENCES exercise_plan(exercise_id) ON DELETE CASCADE,
    FOREIGN KEY (workout_plan_id) REFERENCES exercise_plan(workout_plan_id) ON DELETE CASCADE
);

CREATE TABLE training (
    id VARCHAR(36) NOT NULL,
    name VARCHAR(255) NOT NULL,
    created_by_id VARCHAR(36) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    modified_at TIMESTAMP NOT NULL DEFAULT NOW(),

    workout_plan_id VARCHAR(36),
    start_date TIMESTAMP NOT NULL DEFAULT NOW(),
    end_date TIMESTAMP NULL DEFAULT NULL,

    PRIMARY KEY (id),
    FOREIGN KEY (workout_plan_id) REFERENCES workout_plan(id)
);

CREATE TABLE exercise_training (
    exercise_id VARCHAR(36) NOT NULL,
    training_id VARCHAR(36) NOT NULL,

    sets INT NOT NULL,
    repetitions INT NOT NULL,
    weight FLOAT NOT NULL,

    PRIMARY KEY (exercise_id, training_id),
    FOREIGN KEY (exercise_id) REFERENCES exercise(id) ON DELETE CASCADE,
    FOREIGN KEY (training_id) REFERENCES training(id) ON DELETE CASCADE
);