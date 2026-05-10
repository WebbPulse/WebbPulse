# ---------------------------------------------------------------------------
# Backend — ECR repository + App Runner service
#
# Bootstrap order:
#   1. Run `terraform apply -target=aws_ecr_repository.backend` first
#   2. Build and push your Docker image to the ECR repo
#      (backend/ has no Dockerfile yet — create one that runs uvicorn on :8000)
#   3. Run full `terraform apply` to deploy App Runner
#
# After initial deploy, image updates are handled by CI/CD pushing to ECR
# and triggering an App Runner deployment — Terraform ignores the image tag.
# ---------------------------------------------------------------------------

resource "aws_ecr_repository" "backend" {
  name                 = "${local.prefix}-backend"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

resource "aws_ecr_lifecycle_policy" "backend" {
  repository = aws_ecr_repository.backend.name

  policy = jsonencode({
    rules = [{
      rulePriority = 1
      description  = "Keep last 3 images"
      selection = {
        tagStatus   = "any"
        countType   = "imageCountMoreThan"
        countNumber = 3
      }
      action = { type = "expire" }
    }]
  })
}

# ---------------------------------------------------------------------------
# IAM — ECR pull role (used by App Runner control plane during builds)
# ---------------------------------------------------------------------------

resource "aws_iam_role" "apprunner_ecr_access" {
  name = "${local.prefix}-apprunner-ecr-access"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "build.apprunner.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy_attachment" "apprunner_ecr_access" {
  role       = aws_iam_role.apprunner_ecr_access.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSAppRunnerServicePolicyForECRAccess"
}

# ---------------------------------------------------------------------------
# IAM — instance role (used by the running container to read SSM secrets)
# ---------------------------------------------------------------------------

resource "aws_iam_role" "apprunner_instance" {
  name = "${local.prefix}-apprunner-instance"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "tasks.apprunner.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy" "apprunner_ssm" {
  name = "ssm-read"
  role = aws_iam_role.apprunner_instance.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect   = "Allow"
      Action   = ["ssm:GetParameters", "ssm:GetParameter"]
      Resource = "arn:aws:ssm:${var.aws_region}:${data.aws_caller_identity.current.account_id}:parameter/${local.prefix}/*"
    }]
  })
}

# ---------------------------------------------------------------------------
# App Runner service
# App Runner uses default (AWS-managed) egress. It reaches RDS over the
# public internet via the endpoint's DNS name; auth + SSL secure the link.
# ---------------------------------------------------------------------------

resource "aws_apprunner_service" "backend" {
  service_name = "${local.prefix}-backend"

  source_configuration {
    authentication_configuration {
      access_role_arn = aws_iam_role.apprunner_ecr_access.arn
    }

    image_repository {
      image_identifier      = "${aws_ecr_repository.backend.repository_url}:latest"
      image_repository_type = "ECR"

      image_configuration {
        port = "8000"

        runtime_environment_secrets = {
          DATABASE_URL   = aws_ssm_parameter.database_url.arn
          SECRET_KEY     = aws_ssm_parameter.secret_key.arn
          ADMIN_USERNAME = aws_ssm_parameter.admin_username.arn
          ADMIN_PASSWORD = aws_ssm_parameter.admin_password.arn
          ADMIN_EMAIL    = aws_ssm_parameter.admin_email.arn
        }

        runtime_environment_variables = {
          ENVIRONMENT  = var.environment
          CORS_ORIGINS = "https://www.webbpulse.com,https://webbpulse.com"
        }
      }
    }

    # Deployments triggered by CI/CD pushing to ECR, not by Terraform
    auto_deployments_enabled = false
  }

  instance_configuration {
    cpu               = "0.25 vCPU"
    memory            = "0.5 GB"
    instance_role_arn = aws_iam_role.apprunner_instance.arn
  }

  # Explicit DEFAULT egress. Terraform treats this block as computed, so
  # simply removing it does NOT revert a previously configured VPC egress —
  # the value must be set explicitly to force the switch away from VPC.
  network_configuration {
    egress_configuration {
      egress_type = "DEFAULT"
    }

    ingress_configuration {
      is_publicly_accessible = true
    }
  }

  # CI/CD manages the deployed image tag — don't let Terraform roll it back
  lifecycle {
    ignore_changes = [
      source_configuration[0].image_repository[0].image_identifier,
    ]
  }
}
