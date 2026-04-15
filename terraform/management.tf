# ---------------------------------------------------------------------------
# AWS myApplications — Service Catalog AppRegistry
# Provides a unified console view of all application resources,
# cost breakdown, security findings, and operational data.
# ---------------------------------------------------------------------------
resource "aws_servicecatalogappregistry_application" "webbpulse" {
  name        = local.prefix
  description = "WebbPulse portfolio website"
}

# ---------------------------------------------------------------------------
# Resource Group — tag-based auto-discovery
# Surfaces all Project=webbpulse resources in the console and feeds
# the myApplications view.
# ---------------------------------------------------------------------------
resource "aws_resourcegroups_group" "webbpulse" {
  name        = local.prefix
  description = "All WebbPulse managed resources"

  resource_query {
    query = jsonencode({
      ResourceTypeFilters = ["AWS::AllSupported"]
      TagFilters = [
        {
          Key    = "Project"
          Values = ["webbpulse"]
        }
      ]
    })
  }
}

# ---------------------------------------------------------------------------
# Cost Anomaly Detection — alerts on unexpected spend spikes (free)
# Monitors per AWS service; daily digest when any anomaly >= $10.
# ---------------------------------------------------------------------------
resource "aws_ce_anomaly_monitor" "webbpulse" {
  name         = local.prefix
  monitor_type = "CUSTOM"

  monitor_specification = jsonencode({
    Tags = {
      Key          = "Project"
      Values       = ["webbpulse"]
      MatchOptions = ["EQUALS"]
    }
  })
}

resource "aws_ce_anomaly_subscription" "webbpulse" {
  name      = local.prefix
  frequency = "DAILY"

  monitor_arn_list = [aws_ce_anomaly_monitor.webbpulse.arn]

  subscriber {
    type    = "EMAIL"
    address = "tyler@webbpulse.com"
  }

  subscriber {
    type    = "EMAIL"
    address = "tylert2610@gmail.com"
  }

  threshold_expression {
    dimension {
      key           = "ANOMALY_TOTAL_IMPACT_ABSOLUTE"
      match_options = ["GREATER_THAN_OR_EQUAL"]
      values        = ["10"]
    }
  }
}

# ---------------------------------------------------------------------------
# Budget alerts — first 2 budgets per account are free
# ---------------------------------------------------------------------------
resource "aws_budgets_budget" "warn" {
  name         = "${local.prefix}-monthly-warn"
  budget_type  = "COST"
  limit_amount = "10"
  limit_unit   = "USD"
  time_unit    = "MONTHLY"

  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 100
    threshold_type             = "PERCENTAGE"
    notification_type          = "ACTUAL"
    subscriber_email_addresses = ["tyler@webbpulse.com", "tylert2610@gmail.com"]
  }
}

resource "aws_budgets_budget" "critical" {
  name         = "${local.prefix}-monthly-critical"
  budget_type  = "COST"
  limit_amount = "25"
  limit_unit   = "USD"
  time_unit    = "MONTHLY"

  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 100
    threshold_type             = "PERCENTAGE"
    notification_type          = "ACTUAL"
    subscriber_email_addresses = ["tyler@webbpulse.com", "tylert2610@gmail.com"]
  }
}

# ---------------------------------------------------------------------------
# AppRegistry Attribute Group — enriches the myApplications console view
# with owner and technology metadata.
# ---------------------------------------------------------------------------
resource "aws_servicecatalogappregistry_attribute_group" "webbpulse" {
  name        = "${local.prefix}-metadata"
  description = "Application metadata for WebbPulse"

  attributes = jsonencode({
    owner      = "Tyler Webb"
    email      = "tyler@webbpulse.com"
    repository = "https://github.com/WebbPulse/WebbPulse"
    technology = "FastAPI, PostgreSQL, React"
  })
}

resource "aws_servicecatalogappregistry_attribute_group_association" "webbpulse" {
  application_id     = aws_servicecatalogappregistry_application.webbpulse.id
  attribute_group_id = aws_servicecatalogappregistry_attribute_group.webbpulse.id
}
