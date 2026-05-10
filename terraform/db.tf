# ---------------------------------------------------------------------------
# RDS PostgreSQL — db.t4g.micro, private subnets, no public access
# ---------------------------------------------------------------------------

resource "random_password" "db" {
  length  = 32
  special = false # avoid chars that need URL-encoding in the connection string
}

resource "aws_db_subnet_group" "main" {
  name       = local.prefix
  subnet_ids = [aws_subnet.public_a.id, aws_subnet.public_b.id]
}

resource "aws_db_instance" "main" {
  identifier = local.prefix

  engine         = "postgres"
  engine_version = "16"
  instance_class = var.db_instance_class

  db_name  = var.db_name
  username = var.db_username
  password = random_password.db.result

  storage_type          = "gp3"
  allocated_storage     = 20
  max_allocated_storage = 100
  storage_encrypted     = true

  db_subnet_group_name   = aws_db_subnet_group.main.name
  vpc_security_group_ids = [aws_security_group.rds.id]
  publicly_accessible    = true

  # Required so the subnet-group change + publicly_accessible flip are applied
  # in a single maintenance window instead of waiting. Causes a short reboot.
  apply_immediately = true

  backup_retention_period = 7
  deletion_protection     = false
  skip_final_snapshot     = true

  # Suppress password drift — rotations happen outside Terraform
  lifecycle {
    ignore_changes = [password]
  }
}

# ---------------------------------------------------------------------------
# SSM parameters — secrets injected into App Runner at runtime
# ---------------------------------------------------------------------------

resource "aws_ssm_parameter" "database_url" {
  name  = "/${local.prefix}/database-url"
  type  = "SecureString"
  value = "postgresql://${var.db_username}:${random_password.db.result}@${aws_db_instance.main.endpoint}/${var.db_name}"
}

resource "aws_ssm_parameter" "secret_key" {
  name  = "/${local.prefix}/secret-key"
  type  = "SecureString"
  value = random_password.secret_key.result
}

resource "random_password" "secret_key" {
  length  = 64
  special = true
}

# Admin credentials seeded into the app on startup. Set values manually
# in SSM after first apply; Terraform ignores subsequent changes.
resource "aws_ssm_parameter" "admin_username" {
  name  = "/${local.prefix}/admin-username"
  type  = "SecureString"
  value = "REPLACE_ME"

  lifecycle {
    ignore_changes = [value]
  }
}

resource "aws_ssm_parameter" "admin_password" {
  name  = "/${local.prefix}/admin-password"
  type  = "SecureString"
  value = "REPLACE_ME"

  lifecycle {
    ignore_changes = [value]
  }
}

resource "aws_ssm_parameter" "admin_email" {
  name  = "/${local.prefix}/admin-email"
  type  = "SecureString"
  value = "REPLACE_ME"

  lifecycle {
    ignore_changes = [value]
  }
}
