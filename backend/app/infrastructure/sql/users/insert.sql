INSERT INTO users (id, name, email, created_at, updated_at)
VALUES (:id, :name, :email, :created_at, :updated_at)
ON CONFLICT (id) DO UPDATE SET
    name = :name, email = :email, updated_at = :updated_at
